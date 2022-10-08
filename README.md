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
    