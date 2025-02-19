#!/usr/bin/env python3
import os
import argparse
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def process_audio_file(input_path: str, output_path: str, threshold: float):
    """
    WAV ファイルの音量をチェックし、非無音部分のみの dBFS をもとに、閾値以下なら閾値まで上げて保存する。
    既に閾値以上の場合はそのまま保存する。
    """
    try:
        audio = AudioSegment.from_wav(input_path)
    except Exception as e:
        print(f"ファイルの読み込みに失敗しました: {input_path} ({e})")
        return

    # 無音部分を除いた非無音区間を検出
    # ここでは、最小無音長 100ms、silence_thresh は audio.dBFS から -16dB の値を利用
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=100, silence_thresh=audio.dBFS - 16)

    if nonsilent_ranges:
        # 非無音区間だけを結合して新しい AudioSegment を作成
        non_silent_audio = AudioSegment.empty()
        for start, end in nonsilent_ranges:
            non_silent_audio += audio[start:end]
        effective_dbfs = non_silent_audio.dBFS
    else:
        # 全体が無音に近い場合は、全体の dBFS を利用
        effective_dbfs = audio.dBFS

    # 無音部分を除いた dBFS が None や -inf の場合は処理できないためスキップ
    if effective_dbfs == float("-inf"):
        print(f"無音ファイルのためスキップします: {input_path}")
        return

    # 閾値より低い（つまり音が小さい）場合、必要な分だけ増幅
    if effective_dbfs < threshold:
        # 増幅する量は、差分（閾値 - 非無音部分の dBFS）
        gain_needed = threshold - effective_dbfs
        adjusted_audio = audio.apply_gain(gain_needed)
        print(f"【調整】 {input_path} の非無音部分 dBFS={effective_dbfs:.2f} を閾値 {threshold} まで {gain_needed:.2f}dB 上げます。")
    else:
        adjusted_audio = audio
        print(f"【そのまま】 {input_path} の非無音部分 dBFS={effective_dbfs:.2f} は閾値 {threshold} 以上です。")

    # 出力ディレクトリが存在しなければ作成
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        adjusted_audio.export(output_path, format="wav")
    except Exception as e:
        print(f"ファイルの保存に失敗しました: {output_path} ({e})")

def process_folder(input_dir: str, output_dir: str, threshold: float):
    """
    入力ディレクトリを再帰的に探索し、WAV ファイルを処理する。
    出力先は入力ファイルのフォルダ構造を維持する。
    """
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".wav"):
                input_path = os.path.join(root, file)
                # 入力ディレクトリからの相対パスを算出し、出力先パスに結合
                relative_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, relative_path)
                process_audio_file(input_path, output_path, threshold)

def main():
    parser = argparse.ArgumentParser(description="WAV ファイルの音量を閾値まで上げるプログラム（無音部分を除外）")
    parser.add_argument("--input_dir", required=True, help="入力フォルダパス")
    parser.add_argument("--output_dir", required=True, help="出力フォルダパス")
    parser.add_argument("--threshold", type=float, required=True, help="閾値（dBFS、例: -20）")
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print("指定された入力ディレクトリは存在しません。")
        return

    process_folder(args.input_dir, args.output_dir, args.threshold)
    print("処理が完了しました。")

if __name__ == "__main__":
    main()
