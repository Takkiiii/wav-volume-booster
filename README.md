# WAV Volume Booster

このプロジェクトは、指定したフォルダ内の複数の WAV ファイルの音量を、設定した閾値まで上げるための Python スクリプトです。  
**今回のバージョンでは、無音部分を除いた非無音区間のみで音量評価を行い、実際に聞こえる部分を基に増幅量を決定します。**  
入力フォルダのディレクトリ構造は、出力フォルダにもそのまま維持されます。

## 特徴

- 指定した閾値（dBFS）未満の音量の WAV ファイルに対して、必要な分だけ増幅します。
- **無音部分を除いた非無音区間のみの音量を基に評価するため、無音が多いファイルでも適切な増幅が行われます。**
- 閾値以上の場合はファイルをそのまま出力します。
- 入力フォルダのディレクトリ構造を出力先に再現します。

## 必要なもの

- Python 3.x
- [PyDub](https://github.com/jiaaro/pydub) ライブラリ  
  ```bash
  pip install pydub
  ```
- ffmpeg（Mac の場合は Homebrew でインストール可能）
    ```bash
    brew install ffmpeg
    ```

## 使い方
1. このリポジトリをクローンします。

``` bash
git clone https://github.com/yourusername/wav-volume-threshold.git
cd wav-volume-threshold
```

2. 必要なパッケージをインストールします。

```bash
pip install -r requirements.txt
```

3. スクリプトを実行します。

```bash
python adjust_volume.py --input_dir /path/to/input_folder --output_dir /path/to/output_folder --threshold -20
```

例：
```bash
python adjust_volume.py --input_dir "/Users/takizawa/Downloads/上位店舗" --output_dir "./output" --threshold -20
```
実行後、出力フォルダには同じフォルダ構造が作成され、各 WAV ファイルが音量調整された状態で保存されます。

## 注意事項

- dBFS は通常負の値となります。閾値は例として -20 などの負の値を指定してください。
- 無音ファイルの場合、dBFS は -inf になるため、その場合は処理がスキップされます。
