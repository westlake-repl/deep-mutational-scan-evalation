# deep-mutational-scan-evalation

    收集DeepSequence文献中的数据，提供一个统一的测试方法

## 统一数据视图

    使用DeepSequence数据用手动收集了其wildtype以及其mut-fitness的数据

    运行`ETL.ipynb`后可以获得`data`文件夹，下面包含了经过处理之后的数据

### 一部分数据缺失

    由于水平和时间限制，一些数据库并没有找到对应的wildtype，如下：

    - parEparD_Laub2015_all
    - BG_STRSQ_hmmerbit
    - tRNA_mutation_effect
    - HG_FLU_Bloom2016
    - TIM_SULSO_b0
    - PA_FLU_Sun2015
    - POL_HV1N5-CA_Ndungu2014

### 数据总体上共有37组

    总体上去除了找不到wt的数据集，剩下还剩37组数据
    另外，数据集中描述为stablized的数据集，其wildtype均使用的是未经过stablized的数据集

### 数据集特殊情况

    数据集中存在几种情况无法处理
    - wildtype长度超过1022，ESM1v无法存储
    - 多点突变
    - 数据集中有WT，与其他形式格式不同
    - 找到的sequence与csv中的不完全对应，需要进行修改

    具体调整如下：
    - POLG_HCVJF_Sun2014: wildtype长度超过1022
    - PTEN_HUMAN_Fowler2018: 最后有一项是WT，需要手动在数据集里面删掉
    - PABP_YEAST_Fields2013-doubles: 双点突变，暂时处理不了
    - BRCA1_HUMAN_RING: wildtype长度超过1022
    - MTH3_HAEAESTABILIZED_Tawfik2015: 第26号位置csv中是A，而sequence中是C。并且由于这个是Stabilized，所以我们相信csv中的标记，将sequence改为A；同理104号将sequence的I改为K；115 M到L；181 F到L；327 C到R
    - UBC9_HUMAN_Roth2017: csv中159号位置有一个Y，但是sequence中没有，所以给sequence最后加入一个Y
    - UBE4B_MOUSE_Klevit2013-singles: 长度超过1022
    - TIM_THEMA_b0: 102号位置 C换成S
    - F7YBW7_MESOW_vae: 四点突变，暂时不处理
    - B3VI55_LIPSTSTABLE: 140号位置L变成I，142号位置从S变成A，373号位置A变成C
    - HIS7_YEAST_Kondrashov2017: 多点同时突变，暂时不处理
    - BRCA1_HUMAN_BRCT: 长度超过1022
    - TPMT_HUMAN_Fowler2018: 最后有一项是WT，需要手动在数据集里面删掉

    因此，这里将经过处理的可以直接运行的data上传

## 安装

    conda env create -f enviroment.yaml

## 处理K50_dG数据集

- 数据集来自于：[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7401275.svg)](https://doi.org/10.5281/zenodo.7401275)
- 文章来自于: [![DOI](https://zenodo.org/badge/DOI/10.1101/2022.12.06.519132.svg)](https://doi.org/10.1101/2022.12.06.519132)
- 将[数据集](https://zenodo.org/record/7401275/files/Processed_K50_dG_datasets.zip?download=1)下载，解压后放在`Processed_K50_dG_datasets`文件夹下

```bash
python process_data.py -i Processed_K50_dG_datasets/K50_dG_Dataset1_Dataset2.csv -o Processed_K50_dG_datasets/data -fc deltaG
```
