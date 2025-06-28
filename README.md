# Create-gene-sharing-Network-of-bacterial-genome
バクテリアゲノムのオーソログの情報から遺伝子の共有ネットワークを作成するpythonプログラム


# LAB(lactic acid bacteria) 系統間オルソログネットワーク解析

## 概要

このリポジトリは、細菌株間のオルソログ共有に基づくネットワーク解析のためのPythonスクリプトを含んでいます。主に以下の3つの機能を提供します。

1. **株間のオルソログ共有ネットワークの構築**  
2. **ネットワークからのコミュニティ抽出**  
3. **抽出したコミュニティのテキストファイルを表形式に変換**

---

## ファイル構成

```
├── 20210406_create_networks_generalist_specialist.py
├── 20210408_community_extraction.py
├── 20210512_community_extractionfile_to_table.py
├── README.md
```

---

## スクリプトの説明

### 1. `20210406_create_networks_generalist_specialist.py`

**概要：**  
株間のオルソログ共有数に基づいてネットワークを構築します。表現型データを元に、「ジェネラリスト」と「スペシャリスト」の株グループに分類してネットワークを作成します。

**主な機能：**
- オルソログカウントテーブルの読み込み
- 株ペア間の共有オルソログ数の計算
- ジェネラリストとスペシャリストのネットワークエッジリストを出力
- 系統の属レベルのカラーマッピング情報も付与

**出力ファイル例：**
- `sharing_ortholog_number_more_than;X_generalist.tsv`
- `sharing_ortholog_number_more_than;X_specialist.tsv`
- `sharing_ortholog_number_more_than;X_generalist_specialist_others.tsv`
- `sharing_ortholog_number_more_than;X_strain_table_plus_colorcode.tsv`
- `network image`
![Image](https://github.com/user-attachments/assets/7ed34832-1a9b-45ec-b4c5-5c099376a39a)---

### 2. `20210408_community_extraction.py`

**概要：**  
ネットワークから最大クリーク（clique）を探索し、コミュニティとして抽出します。

**主な機能：**
- ネットワークの可視化
- 最大クリークをコミュニティとして抽出
- 各コミュニティの属レベルの組成を出力

**出力ファイル例：**
- `community_extraction_of_generalist.txt`：各コミュニティの属およびメンバーの詳細
- `community_extraction_of_generalist_only_genus.txt`：属のみの組み合わせに注目したサマリー

---

### 3. `20210512_community_extractionfile_to_table.py`

**概要：**  
テキスト形式のコミュニティ抽出結果（`community_extraction_of_generalist.txt`）を、表形式（TSV）に変換します。論文のサプリメント資料などへの利用を想定しています。

**出力ファイル例：**
- `table_s2.tsv`：コミュニティID、株数、属のリスト、メンバーのリストを含むタブ区切りテーブル

---

## 動作環境

- Python バージョン 3.6 以上
- 必要なライブラリ：
  - `pandas`
  - `numpy`
  - `networkx`
  - `matplotlib`


## 実行方法

### 実行の流れ：

1. **ネットワークの作成**
```bash
python 20210406_create_networks_generalist_specialist.py
```

2. **コミュニティ抽出**
```bash
python 20210408_community_extraction.py
```

3. **テーブルへの変換**
```bash
python 20210512_community_extractionfile_to_table.py
```

※ 各スクリプト内のファイルパスは実行前に適宜修正してください。

---

## ライセンス

MITライセンスのもとで公開しています。

---

## 作者

Takenaka Shinkuro (2021) 本ツールは次の論文の解析の一部として開発されました。

Shinkuro Takenaka, Takeshi Kawashima, Masanori Arita, A sugar utilization phenotype contributes to the formation of genetic exchange communities in lactic acid bacteria, FEMS Microbiology Letters, Volume 368, Issue 17, September 2021, fnab117, https://doi.org/10.1093/femsle/fnab117

---
## 今後の改善案（任意）

- ファイルパスの引数化（`argparse`対応）
- コードコメントの英文化
- テスト用のサンプルデータ追加
