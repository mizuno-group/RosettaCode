# Rosetta Ligand Docking with Rosettascripts

### ligand preparation

1. ligandファイル(**sdf**)を準備
- PDBからのインストール、RDKitによる準備が可能
- .pdbで準備すると以降回らないコードがある
- SMILESから準備する場合は`scripts/smiles2sdf.py`で変換

2. ConformerGeneratorのインストール
BCL::Confからインストール用のshファイルをダウンロードし、展開。ライセンスが必要。
- ライセンスファイルは実行ファイルと同じディレクトリに入れておく

3. ConformerGeneratorでligand conformerを生成
- Rosettaはligandの配座を変形しないため、ConformerGeneratorを用いてあらかじめ複数の3次元配座を生成しておく。`ConformarGenerator.sh`から実行可能。


### protein preparation

1. PDBファイルの準備
- PDBからダウンロードするのが最速
- PyMOLを使用して余計な低分子(結晶化のための長鎖アルコールなど)、水、余計なサブタイプを除く
- もしくは`scripts/exract_ligand.py --remove_chain`から除ける

2. Relax
- タンパク質をligand freeな状態でエネルギー最適化する
- `scripts/prepare_protein.sh`を参照

### Ligand Docking

- pythonコードを含むため仮想環境をアクティベートしておく
- `execute_vs.sh` 参照
- とにかくオプションやxmlの選択肢が多いことに留意する。参照サイトはRosettaScripts.mdに記載しているが、目的意識を持って読まないとわけが分からなくなる。

### 後解析
- `sc_parser.sh` で Rosetta score file を csv に変換する
- `select_score.py` で ファイルをスコア順で選定する