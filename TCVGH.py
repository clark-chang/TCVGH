#!/usr/bin/env python
# coding: utf-8

# 

# In[ ]:


#1.輸入套件
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import os
import warnings


# In[ ]:


#2.忽略警告
sns.set_style("whitegrid")
warnings.filterwarnings("ignore")


# In[ ]:


#3.展開行列
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


# In[ ]:


#4.確認路徑
os.chdir(os.path.dirname(__file__))
print(os.getcwd())


# In[ ]:


#5.讀取主檔
datamain = pd.read_csv(filepath_or_buffer = ".//1.data_main.csv",
                       encoding = "big5",
                       parse_dates = ["Go_hospital_date(Emergency)", "Discharge_date"])


# In[ ]:


#6.複製主檔
main = datamain.copy()


# In[ ]:


#7.計算outcome
main["hours"] = (main["Discharge_date"] - main["Go_hospital_date(Emergency)"]) // pd.Timedelta("1h")

main.insert(len(main.columns), column = "outcome", value = None)

for label, content in main["hours"].iteritems():
    if content <= 168:
        main.loc[label, "outcome"] = 1
    elif content > 168:
        main.loc[label, "outcome"] = 0
outcome = pd.Series(main["outcome"], dtype=int).reset_index(drop=True)


# In[ ]:


#8.讀取共病
comorbidity = pd.read_csv(filepath_or_buffer = ".//4.comorbidity.csv")


# In[ ]:


#9.讀取用藥
medicine1d = pd.read_excel(io = ".//5.1dmedicine.xlsx")
medicine2d = pd.read_excel(io = ".//5.2dmedicine.xlsx")
medicine3d = pd.read_excel(io = ".//5.3dmedicine.xlsx")

medicine1d = pd.get_dummies(medicine1d)
medicine1d = medicine1d.groupby("Serial_number", as_index = False).max()
medicine1d.replace(0, "N", inplace = True)
medicine1d.replace(1, "Y", inplace = True)
medicine2d = pd.get_dummies(medicine2d)
medicine2d = medicine2d.groupby("Serial_number", as_index = False).max()
medicine2d.replace(0, "N", inplace = True)
medicine2d.replace(1, "Y", inplace = True)
medicine3d = pd.get_dummies(medicine3d)
medicine3d = medicine3d.groupby("Serial_number", as_index = False).max()
medicine3d.replace(0, "N", inplace = True)
medicine3d.replace(1, "Y", inplace = True)


# In[ ]:


#10.讀取飲酒
drink = pd.read_excel(io = ".//6.drink.xlsx")


# In[ ]:


#11.讀取抽菸
smoke = pd.read_excel(io = ".//7.smoke.xlsx")


# In[ ]:


#12.讀取加護病房檔
cu = pd.read_csv(filepath_or_buffer = ".//10.cu.csv")


# In[ ]:


#13.讀取住院科別
section = pd.read_csv(filepath_or_buffer = ".//11.admission.csv", encoding = "big5")


# In[ ]:


#14.讀取醫師
dr = pd.read_csv(filepath_or_buffer = ".//12.Dr.csv", encoding = "big5")


# In[ ]:


#15.讀取連續24小時檢驗檢查檔
bt24 = pd.read_csv(filepath_or_buffer = ".//9.1.bt24.csv")
pulse24 = pd.read_csv(filepath_or_buffer = ".//9.2.pulse24.csv")
rr24 = pd.read_csv(filepath_or_buffer = ".//9.3.rr24.csv")
sbp24 = pd.read_csv(filepath_or_buffer = ".//9.4.sbp24.csv")
pao224 = pd.read_csv(filepath_or_buffer = ".//9.5.pao224.csv")


# In[ ]:


#16.讀取檢驗檢查檔&急診用藥藥價(antibiotic)
ca1 = pd.read_csv(filepath_or_buffer = ".//8.1.1Ca.csv")
ca2 = pd.read_csv(filepath_or_buffer = ".//8.2.1Ca.csv")
ca3 = pd.read_csv(filepath_or_buffer = ".//8.3.1Ca.csv")
ph1 = pd.read_csv(filepath_or_buffer = ".//8.1.2pH.csv")
ph2 = pd.read_csv(filepath_or_buffer = ".//8.2.2pH.csv")
ph3 = pd.read_csv(filepath_or_buffer = ".//8.3.2pH.csv")
ttp1 = pd.read_csv(filepath_or_buffer = ".//8.1.3TTP.csv")
ttp2 = pd.read_csv(filepath_or_buffer = ".//8.2.3TTP.csv")
ttp3 = pd.read_csv(filepath_or_buffer = ".//8.3.3TTP.csv")
alb1 = pd.read_csv(filepath_or_buffer = ".//8.1.4Alb.csv")
alb2 = pd.read_csv(filepath_or_buffer = ".//8.2.4Alb.csv")
alb3 = pd.read_csv(filepath_or_buffer = ".//8.3.4Alb.csv")
bilt1 = pd.read_csv(filepath_or_buffer = ".//8.1.5BILT.csv")
bilt2 = pd.read_csv(filepath_or_buffer = ".//8.2.5BILT.csv")
bilt3 = pd.read_csv(filepath_or_buffer = ".//8.3.5BILT.csv")
got1 = pd.read_csv(filepath_or_buffer = ".//8.1.6GOT.csv")
got2 = pd.read_csv(filepath_or_buffer = ".//8.2.6GOT.csv")
got3 = pd.read_csv(filepath_or_buffer = ".//8.3.6GOT.csv")
gpt1 = pd.read_csv(filepath_or_buffer = "8.1.7GPT.csv")
gpt2 = pd.read_csv(filepath_or_buffer = "8.2.7GPT.csv")
gpt3 = pd.read_csv(filepath_or_buffer = "8.3.7GPT.csv")
alkp1 = pd.read_csv(filepath_or_buffer = ".//8.1.8ALKP.csv")
alkp2 = pd.read_csv(filepath_or_buffer = ".//8.2.8ALKP.csv")
alkp3 = pd.read_csv(filepath_or_buffer = ".//8.3.8ALKP.csv")
wbc1 = pd.read_csv(filepath_or_buffer = ".//8.1.9WBC.csv")
wbc2 = pd.read_csv(filepath_or_buffer = ".//8.2.9WBC.csv")
wbc3 = pd.read_csv(filepath_or_buffer = ".//8.3.9WBC.csv")
hgb1 = pd.read_csv(filepath_or_buffer = ".//8.1.10HGB.csv")
hgb2 = pd.read_csv(filepath_or_buffer = ".//8.2.10HGB.csv")
hgb3 = pd.read_csv(filepath_or_buffer = ".//8.3.10HGB.csv")
plt1 = pd.read_csv(filepath_or_buffer = "8.1.11PLT.csv")
plt2 = pd.read_csv(filepath_or_buffer = "8.2.11PLT.csv")
plt3 = pd.read_csv(filepath_or_buffer = "8.3.11PLT.csv")
na1 = pd.read_csv(filepath_or_buffer = ".//8.1.12Na.csv")
na2 = pd.read_csv(filepath_or_buffer = ".//8.2.12Na.csv")
na3 = pd.read_csv(filepath_or_buffer = ".//8.3.12Na.csv")
k1 = pd.read_csv(filepath_or_buffer = ".//8.1.13K.csv")
k2 = pd.read_csv(filepath_or_buffer = ".//8.2.13K.csv")
k3 = pd.read_csv(filepath_or_buffer = ".//8.3.13K.csv")
cl1 = pd.read_csv(filepath_or_buffer = "8.1.14CL.csv")
cl2 = pd.read_csv(filepath_or_buffer = "8.2.14CL.csv")
cl3 = pd.read_csv(filepath_or_buffer = "8.3.14CL.csv")
bun1 = pd.read_csv(filepath_or_buffer = "8.1.15BUN.csv")
bun2 = pd.read_csv(filepath_or_buffer = "8.2.15BUN.csv")
bun3 = pd.read_csv(filepath_or_buffer = "8.3.15BUN.csv")
cr1 = pd.read_csv(filepath_or_buffer = ".//8.1.16Cr.csv")
cr2 = pd.read_csv(filepath_or_buffer = ".//8.2.16Cr.csv")
cr3 = pd.read_csv(filepath_or_buffer = ".//8.3.16Cr.csv")
crp1 = pd.read_csv(filepath_or_buffer = ".//8.1.17CRP.csv")
crp2 = pd.read_csv(filepath_or_buffer = ".//8.2.17CRP.csv")
crp3 = pd.read_csv(filepath_or_buffer = ".//8.3.17CRP.csv")
glu1 = pd.read_csv(filepath_or_buffer = ".//8.1.18Glu.csv")
glu2 = pd.read_csv(filepath_or_buffer = ".//8.2.18Glu.csv")
glu3 = pd.read_csv(filepath_or_buffer = ".//8.3.18Glu.csv")
pao21 = pd.read_csv(filepath_or_buffer = ".//8.1.21PaO2.csv")
pao22 = pd.read_csv(filepath_or_buffer = ".//8.2.21PaO2.csv")
pao23 = pd.read_csv(filepath_or_buffer = ".//8.3.21PaO2.csv")
pct1 = pd.read_csv(filepath_or_buffer = ".//8.1.22PCT.csv")
pct2 = pd.read_csv(filepath_or_buffer = ".//8.2.22PCT.csv")
pct3 = pd.read_csv(filepath_or_buffer = ".//8.3.22PCT.csv")
rr1 = pd.read_csv(filepath_or_buffer = ".//8.1.23RR.csv")
rr2 = pd.read_csv(filepath_or_buffer = ".//8.2.23RR.csv")
rr3 = pd.read_csv(filepath_or_buffer = ".//8.3.23RR.csv")
sbp1 = pd.read_csv(filepath_or_buffer = ".//8.1.24SBP.csv")
sbp2 = pd.read_csv(filepath_or_buffer = ".//8.2.24SBP.csv")
sbp3 = pd.read_csv(filepath_or_buffer = ".//8.3.24SBP.csv")
dbp1 = pd.read_csv(filepath_or_buffer = ".//8.1.25DBP.csv")
dbp2 = pd.read_csv(filepath_or_buffer = ".//8.2.25DBP.csv")
dbp3 = pd.read_csv(filepath_or_buffer = ".//8.3.25DBP.csv")
oneglu1 = pd.read_csv(filepath_or_buffer = ".//8.1.26Oneglu.csv")
oneglu2 = pd.read_csv(filepath_or_buffer = ".//8.2.26Oneglu.csv")
oneglu3 = pd.read_csv(filepath_or_buffer = ".//8.3.26Oneglu.csv")
pulse1 = pd.read_csv(filepath_or_buffer = ".//8.1.27Pulse.csv")
pulse2 = pd.read_csv(filepath_or_buffer = ".//8.2.27Pulse.csv")
pulse3 = pd.read_csv(filepath_or_buffer = ".//8.3.27Pulse.csv")
antibiotic1 = pd.read_csv(filepath_or_buffer = ".//8.1.28Antibiotic.csv")
antibiotic2 = pd.read_csv(filepath_or_buffer = ".//8.2.28Antibiotic.csv")
antibiotic3 = pd.read_csv(filepath_or_buffer = ".//8.3.28Antibiotic.csv")
hct1 = pd.read_csv(filepath_or_buffer = ".//8.1.29HCT.csv")
hct2 = pd.read_csv(filepath_or_buffer = ".//8.2.29HCT.csv")
hct3 = pd.read_csv(filepath_or_buffer = ".//8.3.29HCT.csv")
bt1 = pd.read_csv(filepath_or_buffer = ".//8.1.30BT.csv")
bt2 = pd.read_csv(filepath_or_buffer = ".//8.2.30BT.csv")
bt3 = pd.read_csv(filepath_or_buffer = ".//8.3.30BT.csv")


# In[ ]:


#17.讀取PSI指數
psi = pd.read_csv(".//14.PSI.csv")


# In[ ]:


#18.讀取意識混淆
confusion = pd.read_csv(".//15.confusion.csv")


# In[ ]:


#19.建立質量主檔
data_quality = pd.DataFrame({"Serial_number": main["Serial_number"],
                             "Sex": main["Sex"],
                             "Readmission(before 3 days)": main["Readmission(before 3 days )"],
                             "Regist_dapartment(Emergency)": main["Regist_department(Emergency)"],
                             "Regist(EmergencyI1)": main["Regist(EmergencyI1)"],
                             "Regist(EmergencyI2)": main["Regist(EmergencyI2)"],
                             "Leave_department(Emergency)": main["Leave_department(Emergency)"],
                             "Leave(EmergencyI1)": main["Leave(EmergencyI1)"],
                             "Leave(EmergencyI2)": main["Leave(EmergencyI2)"]})


# In[ ]:


#20.合併住院科別
data_quality = data_quality.merge(right = section,
                                  how = "left",
                                  on = "Serial_number")


# In[ ]:


#21.合併醫師
data_quality = data_quality.merge(right = dr,
                                  how = "left",
                                  on = "Serial_number")


# In[ ]:


#22.合併加護病房
data_quality = data_quality.merge(right = cu,
                                  how = "left",
                                  on = "Serial_number")


# In[ ]:


#23.合併共病
data_quality = data_quality.merge(right = comorbidity,
                                  how = "left",
                                  on = "Serial_number")


# In[ ]:


#24.合併用藥
data_quality = data_quality.merge(right = medicine1d,
                                  how = "left",
                                  on = "Serial_number")
data_quality = data_quality.merge(right = medicine2d,
                                  how = "left",
                                  on = "Serial_number")
data_quality = data_quality.merge(right = medicine3d,
                                  how = "left",
                                  on = "Serial_number")


# In[ ]:


#25.合併喝酒
data_quality = data_quality.merge(right = drink,
                                  how = "left",
                                  on = "Serial_number")


# In[ ]:


#26.合併抽菸
data_quality = data_quality.merge(right = smoke,
                                  how = "left",
                                  on = "Serial_number")


# In[ ]:


#27.合併連續24小時正向指標
data_quality = data_quality.merge(right = bt24,
                                  how = "left", 
                                  on = "Serial_number")
data_quality = data_quality.merge(right = pulse24,
                                  how = "left", 
                                  on = "Serial_number")
data_quality = data_quality.merge(right = rr24,
                                  how = "left", 
                                  on = "Serial_number")
data_quality = data_quality.merge(right = sbp24,
                                  how = "left", 
                                  on = "Serial_number")
data_quality = data_quality.merge(right = pao224,
                                  how = "left", 
                                  on = "Serial_number")


# In[ ]:


#28.檢查質量主檔遺漏值
#28.J01類抗生素ATC藥碼補遺漏值
#28.CU補值
print(data_quality.isnull().sum())
data_quality.fillna("N", inplace = True)
print(data_quality.isnull().sum())


# In[ ]:


#29.建立數量主檔
data_quantity = pd.DataFrame({"Serial_number": main["Serial_number"],
                              "Sex": main["Sex"],
                              "Age": main["AGE"]})


# In[ ]:


#30.合併檢驗檢查檔&急診用藥抗生素藥價
data_quantity = data_quantity.merge(right = ca1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = ca2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = ca3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = ph1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = ph2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = ph3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = ttp1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = ttp2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = ttp3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = alb1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = alb2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = alb3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = bilt1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = bilt2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = bilt3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = got1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = got2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = got3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = gpt1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = gpt2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = gpt3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = alkp1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = alkp2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = alkp3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = wbc1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = wbc2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = wbc3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = hgb1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = hgb2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = hgb3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = plt1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = plt2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = plt3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = na1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = na2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = na3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = k1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = k2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = k3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = cl1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = cl2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = cl3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = bun1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = bun2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = bun3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = cr1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = cr2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = cr3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = crp1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = crp2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = crp3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = glu1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = glu2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = glu3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = pao21,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = pao22,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = pao23,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = pct1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = pct2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = pct3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = rr1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = rr2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = rr3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = sbp1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = sbp2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = sbp3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = dbp1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = dbp2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = dbp3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = oneglu1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = oneglu2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = oneglu3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = pulse1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = pulse2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = pulse3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = antibiotic1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = antibiotic2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = antibiotic3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = hct1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = hct2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = hct3,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = bt1,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = bt2,
                                    how = "left",
                                    on = "Serial_number")
data_quantity = data_quantity.merge(right = bt3,
                                    how = "left",
                                    on = "Serial_number")


# In[ ]:


#31.合併混淆(計算Curb-65)
data_quantity = data_quantity.merge(right = confusion,
                                    how = "left",
                                    on = "Serial_number")


# In[ ]:


#32.檢查數量遺漏值
fig, ax = plt.subplots(figsize = (10, 50))
plt.xlabel("Miss Percentage")
plt.ylabel("Feature")
miss = pd.DataFrame({"Feature": list(data_quantity.columns),
                     "Miss Percentage": (data_quantity.isnull().sum() / len(data_quantity)) *100}).sort_values("Miss Percentage")
plt.barh(y = miss["Feature"], width = miss["Miss Percentage"])


# In[ ]:


#33.檢驗檢查補遺漏值
#Ca
data_quantity["1D_Ca_Value"].fillna(9.3, inplace = True)
for label, content in data_quantity["2D_Ca_Value"].iteritems():
    if math.isnan(content):
        data_quantity.at[label, "2D_Ca_Value"] = data_quantity.at[label, "1D_Ca_Value"]
for label, content in data_quantity["3D_Ca_Value"].iteritems():
    if math.isnan(content):
        data_quantity.at[label, "3D_Ca_Value"] = data_quantity.at[label, "2D_Ca_Value"]
#pH
data_quantity["1D_pH_Value"].fillna(7.4, inplace = True)
for label, content in data_quantity["2D_pH_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_pH_Value"] = data_quantity.at[label, "1D_pH_Value"]
for label, content in data_quantity["3D_pH_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_pH_Value"] = data_quantity.loc[label, "2D_pH_Value"]
#TTP
data_quantity["1D_TTP_Value"].fillna(7, inplace = True)
for label, content in data_quantity["2D_TTP_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_TTP_Value"] = data_quantity.loc[label, "1D_TTP_Value"]
for label, content in data_quantity["3D_TTP_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_TTP_Value"] = data_quantity.loc[label, "2D_TTP_Value"]
#Alb
data_quantity["1D_Alb_Value"].fillna(4.25, inplace = True)
for label, content in data_quantity["2D_Alb_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_Alb_Value"] = data_quantity.loc[label, "1D_Alb_Value"]
for label, content in data_quantity["3D_Alb_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_Alb_Value"] = data_quantity.loc[label, "2D_Alb_Value"]        
#BILT
data_quantity["1D_BILT_Value"].fillna(0.7, inplace = True)
for label, content in data_quantity["2D_BILT_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_BILT_Value"] = data_quantity.loc[label, "1D_BILT_Value"]
for label, content in data_quantity["2D_BILT_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_BILT_Value"] = data_quantity.loc[label, "1D_BILT_Value"]
for label, content in data_quantity["3D_BILT_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_BILT_Value"] = data_quantity.loc[label, "2D_BILT_Value"]
#GOT
data_quantity["1D_GOT_Value"].fillna(23, inplace = True)
for label, content in data_quantity["2D_GOT_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_GOT_Value"] = data_quantity.loc[label, "1D_GOT_Value"]
for label, content in data_quantity["3D_GOT_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_GOT_Value"] = data_quantity.loc[label, "2D_GOT_Value"]
#GPT
for index, data in data_quantity.iterrows():
    if math.isnan(data["1D_GPT_Value"]):
        if data["Sex"] == "M":
            data_quantity.loc[index, "1D_GPT_Value"] = 30
        elif data["Sex"] == "F":
            data_quantity.loc[index, "1D_GPT_Value"] = 22.5
for label, content in data_quantity["2D_GPT_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_GPT_Value"] = data_quantity.loc[label, "1D_GPT_Value"]
for label, content in data_quantity["3D_GPT_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_GPT_Value"] = data_quantity.loc[label, "2D_GPT_Value"]        
#ALKP
data_quantity["1D_ALKP_Value"].fillna(120, inplace = True)
for label, content in data_quantity["2D_ALKP_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_ALKP_Value"] = data_quantity.loc[label, "1D_ALKP_Value"]
for label, content in data_quantity["3D_ALKP_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_ALKP_Value"] = data_quantity.loc[label, "2D_ALKP_Value"]     
#WBC
data_quantity["1D_WBC_Value"].fillna(7250, inplace = True)
for label, content in data_quantity["2D_WBC_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_WBC_Value"] = data_quantity.loc[label, "1D_WBC_Value"]
for label, content in data_quantity["3D_WBC_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_WBC_Value"] = data_quantity.loc[label, "2D_WBC_Value"]        
#HGB
for index, rows in data_quantity.iterrows():
    if math.isnan(rows["1D_HGB_Value"]):
        if rows["Sex"] == "M":
            data_quantity.at[index, "1D_HGB_Value"] = 15.5 
        elif rows["Sex"] == "F":
            data_quantity.at[index, "1D_HGB_Value"] = 14
for label, content in data_quantity["2D_HGB_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_HGB_Value"] = data_quantity.loc[label, "1D_HGB_Value"]
for label, content in data_quantity["3D_HGB_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_HGB_Value"] = data_quantity.loc[label, "2D_HGB_Value"]            
#PLT
data_quantity["1D_PLT_Value"].fillna(275, inplace = True)
for label, content in data_quantity["2D_PLT_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_PLT_Value"] = data_quantity.loc[label, "1D_PLT_Value"]
for label, content in data_quantity["3D_PLT_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_PLT_Value"] = data_quantity.loc[label, "2D_PLT_Value"]
#Na
data_quantity["1D_Na_Value"].fillna(145, inplace = True)
for label, content in data_quantity["2D_Na_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_Na_Value"] = data_quantity.loc[label, "1D_Na_Value"]
for label, content in data_quantity["3D_Na_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_Na_Value"] = data_quantity.loc[label, "2D_Na_Value"]
#K
data_quantity["1D_K_Value"].fillna(4.4, inplace = True)
for label, content in data_quantity["2D_K_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_K_Value"] = data_quantity.loc[label, "1D_K_Value"]
for label, content in data_quantity["3D_K_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_K_Value"] = data_quantity.loc[label, "2D_K_Value"] 
#Cl
data_quantity["1D_Cl_Value"].fillna(100, inplace = True)
for label, content in data_quantity["2D_Cl_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_Cl_Value"] = data_quantity.loc[label, "1D_Cl_Value"]
for label, content in data_quantity["3D_Cl_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_Cl_Value"] = data_quantity.loc[label, "2D_Cl_Value"]
#Bun
data_quantity["1D_BUN_Value"].fillna(15, inplace = True)
for label, content in data_quantity["2D_BUN_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_BUN_Value"] = data_quantity.loc[label, "1D_BUN_Value"]
for label, content in data_quantity["3D_BUN_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_BUN_Value"] = data_quantity.loc[label, "2D_BUN_Value"]
#Cr
for index, data in data_quantity.iterrows():
    if math.isnan(data["1D_Cr_Value"]):
        if data["Sex"] == "M":
            data_quantity.loc[index, "1D_Cr_Value"] = 1.05
        elif data["Sex"] == "F":
            data_quantity.loc[index, "1D_Cr_Value"] = 0.7  
for label, content in data_quantity["2D_Cr_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_Cr_Value"] = data_quantity.loc[label, "1D_Cr_Value"]
for label, content in data_quantity["3D_Cr_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_Cr_Value"] = data_quantity.loc[label, "2D_Cr_Value"]
#CRP
data_quantity["1D_CRP_Value"].fillna(0.15, inplace = True)
for label, content in data_quantity["2D_CRP_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_CRP_Value"] = data_quantity.loc[label, "1D_CRP_Value"]
for label, content in data_quantity["3D_CRP_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_CRP_Value"] = data_quantity.loc[label, "2D_CRP_Value"]
#Glu
data_quantity["1D_Glu_Value"].fillna(95, inplace = True)
for label, content in data_quantity["2D_Glu_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_Glu_Value"] = data_quantity.loc[label, "1D_Glu_Value"]
for label, content in data_quantity["3D_Glu_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_Glu_Value"] = data_quantity.loc[label, "2D_Glu_Value"]
#PaO2
data_quantity["1D_PaO2_Value"].fillna(90, inplace = True)
for label, content in data_quantity["2D_PaO2_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_PaO2_Value"] = data_quantity.loc[label, "1D_PaO2_Value"]
for label, content in data_quantity["3D_PaO2_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_PaO2_Value"] = data_quantity.loc[label, "2D_PaO2_Value"]
#PCT
data_quantity["1D_PCT_Value"].fillna(0.099, inplace = True)
for label, content in data_quantity["2D_PCT_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_PCT_Value"] = data_quantity.loc[label, "1D_PCT_Value"]
for label, content in data_quantity["3D_PCT_Value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_PCT_Value"] = data_quantity.loc[label, "2D_PCT_Value"]
#RR
for label, content in data_quantity["3D_RR_value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_RR_value"] = data_quantity.loc[label, "2D_RR_value"]
#SBP
for label, content in data_quantity["2D_SBP_value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_SBP_value"] = data_quantity.loc[label, "1D_SBP_value"]
for label, content in data_quantity["3D_SBP_value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_SBP_value"] = data_quantity.loc[label, "2D_SBP_value"]
#DBP
for label, content in data_quantity["2D_DBP_value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_DBP_value"] = data_quantity.loc[label, "1D_DBP_value"]
for label, content in data_quantity["3D_DBP_value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_DBP_value"] = data_quantity.loc[label, "2D_DBP_value"]
#Oneglu
data_quantity["1D_ONEGLU_value"].fillna(95, inplace = True)
for label, content in data_quantity["2D_ONEGLU_value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_ONEGLU_value"] = data_quantity.loc[label, "1D_ONEGLU_value"]
for label, content in data_quantity["3D_ONEGLU_value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_ONEGLU_value"] = data_quantity.loc[label, "2D_ONEGLU_value"]
#Pulse
for label, content in data_quantity["3D_Pulse_value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_Pulse_value"] = data_quantity.loc[label, "2D_Pulse_value"]
#HCT
for index, data in data_quantity.iterrows():
    if math.isnan(data["1D_HCT_value"]):
        if data["Sex"] == "M":
            data_quantity.loc[index, "1D_HCT_value"] = 46
        elif data["Sex"] == "F":
            data_quantity.loc[index, "1D_HCT_value"] = 42
for label, content in data_quantity["2D_HCT_value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "2D_HCT_value"] = data_quantity.loc[label, "1D_HCT_value"]
for label, content in data_quantity["3D_HCT_value"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_HCT_value"] = data_quantity.loc[label, "2D_HCT_value"]
#BT
for label, content in data_quantity["3D_BT_MIN"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_BT_MIN"] = data_quantity.loc[label, "2D_BT_MIN"]
for label, content in data_quantity["3D_BT_MAX"].iteritems():
    if math.isnan(content):
        data_quantity.loc[label, "3D_BT_MAX"] = data_quantity.loc[label, "2D_BT_MAX"]


# In[ ]:


#34.急診用藥抗生素藥價補遺漏值
fill_antibiotic_price = {"1D_antibiotic_price": 0,
                         "2D_antibiotic_price": 0,
                         "3D_antibiotic_price": 0}
data_quantity.fillna(value = fill_antibiotic_price, inplace = True)


# In[ ]:


#35.意識混淆補值
data_quantity.fillna({"confusion_1d": "N",
                      "confusion_2d": "N",
                      "confusion_3d": "N"}, inplace = True)


# In[ ]:


#36.檢查遺漏值
print(data_quantity.isnull().sum())


# In[ ]:


#37.計算CURB-65
data_quantity.insert(len(data_quantity.columns), "1D_CURB-65", value = 0)
data_quantity.insert(len(data_quantity.columns), "2D_CURB-65", value = 0)
data_quantity.insert(len(data_quantity.columns), "3D_CURB-65", value = 0)

for index, data in data_quantity.iterrows():
    #1D
    if data["1D_BUN_Value"] > 20:
        data_quantity.loc[index, "1D_CURB-65"] += 1 
    if data["1D_RR_value"] >= 30:
        data_quantity.loc[index, "1D_CURB-65"] += 1
    if data["1D_SBP_value"] < 90 or data["1D_DBP_value"] <= 60:
        data_quantity.loc[index, "1D_CURB-65"] += 1
    if data["Age"] >= 65:
        data_quantity.loc[index, "1D_CURB-65"] += 1
    if data["confusion_1d"] == "Y":
        data_quantity.loc[index, "1D_CURB-65"] += 1
    #2D
    if data["2D_BUN_Value"] > 20:
        data_quantity.loc[index, "2D_CURB-65"] += 1 
    if data["2D_RR_value"] >= 30:
        data_quantity.loc[index, "2D_CURB-65"] += 1
    if data["2D_SBP_value"] < 90 or data["2D_DBP_value"] <= 60:
        data_quantity.loc[index, "2D_CURB-65"] += 1
    if data["Age"] >= 65:
        data_quantity.loc[index, "2D_CURB-65"] += 1
    if data["confusion_2d"] == "Y":
        data_quantity.loc[index, "2D_CURB-65"] += 1
    #3D    
    if data["3D_BUN_Value"] > 20:
        data_quantity.loc[index, "3D_CURB-65"] += 1 
    if data["3D_RR_value"] >= 30:
        data_quantity.loc[index, "3D_CURB-65"] += 1
    if data["3D_SBP_value"] < 90 or data["3D_DBP_value"] <= 60:
        data_quantity.loc[index, "3D_CURB-65"] += 1
    if data["Age"] >= 65:
        data_quantity.loc[index, "3D_CURB-65"] += 1
    if data["confusion_3d"] == "Y":
        data_quantity.loc[index, "3D_CURB-65"] += 1        


# In[ ]:


#38.合併PSI指數
data_quantity = data_quantity.merge(right = psi,
                                    how = "left",
                                    on = "Serial_number")


# In[ ]:


#39.計算檢驗檢查變化量
exam_col = 3
for i in range(27):
    data_quantity["2D-1D_change" + "(" + data_quantity.columns[exam_col] + ")"] = data_quantity.iloc[:, exam_col + 1] - data_quantity.iloc[:, exam_col]
    data_quantity["3D-2D_change" + "(" + data_quantity.columns[exam_col] + ")"] = data_quantity.iloc[:, exam_col + 2] - data_quantity.iloc[:, exam_col + 1]
    data_quantity["3D-1D_change" + "(" + data_quantity.columns[exam_col] + ")"] = data_quantity.iloc[:, exam_col + 2] - data_quantity.iloc[:, exam_col]
    exam_col += 3
data_quantity["2D_change_BT_MIN"] = data_quantity["2D_BT_MIN"] - data_quantity["1D_BT_MIN"]
data_quantity["2D_change_BT_MAX"] = data_quantity["2D_BT_MAX"] - data_quantity["1D_BT_MAX"]
data_quantity["3D_change_BT_MIN"] = data_quantity["3D_BT_MIN"] - data_quantity["2D_BT_MIN"]
data_quantity["3D_change_BT_MAX"] = data_quantity["3D_BT_MAX"] - data_quantity["2D_BT_MAX"]


# In[ ]:


#40.移除欄位
"""
data_quality.drop(columns = "Serial_number", inplace = True)
data_quantity.drop(columns = ["Serial_number","Sex", "confusion_1d", "confusion_2d", "confusion_3d"], inplace = True)
"""
data_quantity.drop(columns = ["Sex", "confusion_1d", "confusion_2d", "confusion_3d"], inplace = True)


# In[ ]:


#41.輸出形狀
print(data_quality.shape)
print(data_quantity.shape)


# In[ ]:


#42.質量主檔作get_dummy
data_quality_onehot = pd.get_dummies(data_quality)


# In[ ]:


#43.畫派圖
print(outcome.value_counts()[0], outcome.value_counts()[1])
print(str(0), "Percent", int(outcome.value_counts()[0]/(outcome.value_counts()[0] + outcome.value_counts()[1])*100))
print(str(1), "Percent", int(outcome.value_counts()[1]/(outcome.value_counts()[0] + outcome.value_counts()[1])*100))

x = [outcome.value_counts()[0]/(outcome.value_counts()[0] + outcome.value_counts()[1])*100, outcome.value_counts()[1]/(outcome.value_counts()[0] + outcome.value_counts()[1])*100]
label = ["Admission", "Discharge"]
plt.figure(figsize = (6, 9))
plt.pie(x,
        labels = label,
        autopct = "%.0f%%",
        textprops = {"fontsize": 20})
plt.show()


# In[ ]:


#44.特徵畫data_quality_onehot bar圖
x = ["Total_Data", "Total_Features"]
height = [data_quality_onehot.shape[0], data_quality_onehot.shape[1]]
plt.figure(figsize = (5, 7))
plt.bar(x,
        height)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
plt.title("Data_Quality_Onehot")
plt.show()


# In[ ]:


#45.特徵畫data_quantity bar圖
x = ["Total_Data", "Total_Features"]
height = [data_quantity.shape[0], data_quantity.shape[1]]
plt.figure(figsize = (5, 7))
plt.bar(x,
        height)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)
plt.title("Data_Quantity")
plt.show()


# In[ ]:


#46.輸入套件
from sklearn.feature_selection import SelectFromModel
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import BorderlineSMOTE
from imblearn.over_sampling import KMeansSMOTE#已經無法輸入
from imblearn.over_sampling import SVMSMOTE
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import PowerTransformer
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.svm import SVC
import xgboost as XGB
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import LocalOutlierFactor
from statistics import mean
from sklearn.metrics import classification_report


# In[ ]:


#47.RF取特徵
#data_quality
select_quality = SelectFromModel(RandomForestClassifier(n_estimators = 100,
                                                        random_state = 10,
                                                        ))
select_quality.fit(data_quality_onehot, outcome)
select_quality_report = select_quality.get_support()
select_quality_report = pd.DataFrame({"Feature": list(data_quality_onehot.columns),
                                      "Selection": select_quality_report})
select_data_quality_true = select_quality_report[select_quality_report["Selection"] == True ]["Feature"]
select_data_quality_true_list = list(select_data_quality_true)
#47.RF取特徵
#data_quantity
select_quantity = SelectFromModel(RandomForestClassifier(n_estimators = 100,
                                                        random_state = 10,
                                                        class_weight = "balanced",
                                                        max_features = None))
select_quantity.fit(data_quantity, outcome)
select_quantity_report = select_quantity.get_support()
select_quantity_report = pd.DataFrame({"Feature": list(data_quantity.columns),
                                       "Selection": select_quantity_report})
select_quantity_report_true = select_quantity_report[select_quantity_report["Selection"] == True ]["Feature"]
select_quantity_report_true_list = list(select_quantity_report_true)


# In[ ]:


#48.整理訓練資料
data_outcome = outcome
data_quality_true = data_quality_onehot.loc[:, select_data_quality_true_list]
data_quantity_true = data_quantity.loc[:, select_quantity_report_true_list]
print(data_quality_true.shape)
print(data_quantity_true.shape)


# In[ ]:


#49.資料正規化
#常態分布正規化
pt = PowerTransformer()
pt_data = pt.fit(data_quantity_true)
pt_data = pt_data.transform(data_quantity_true)
pt_data = pd.DataFrame(pt_data)
#最小最大正規化
minmax = MinMaxScaler()
minmax_data = minmax.fit_transform(data_quantity_true)
minmax_data = pd.DataFrame(minmax_data)
#標準化正規化
std = StandardScaler()
std_data = std.fit_transform(data_quantity_true)
std_data = pd.DataFrame(std_data)


# In[ ]:


#50.質量資料及數量資料整合
data_final = pd.DataFrame(index = range(len(outcome)))
pt_data_final = pd.DataFrame(index = range(len(outcome)))
minmax_data_final = pd.DataFrame(index = range(len(outcome)))
std_data_final = pd.DataFrame(index = range(len(outcome)))
#data_final
data_final = data_final.merge(right = data_quantity_true,
                              how = "left", 
                              left_index = True,
                              right_index = True)
data_final = data_final.merge(right = data_quality_true,
                              how = "left",
                              left_index = True,
                              right_index = True)
#pt_data_final
pt_data_final = pt_data_final.merge(right = pt_data,
                                    how = "left", 
                                    left_index = True,
                                    right_index = True)
pt_data_final = pt_data_final.merge(right = data_quality_true,
                                    how = "left",
                                    left_index = True,
                                    right_index = True)
#minmax_data_final
minmax_data_final = minmax_data_final.merge(right = minmax_data,
                                            how = "left", 
                                            left_index = True,
                                            right_index = True)
minmax_data_final = minmax_data_final.merge(right = data_quality_true,
                                            how = "left",
                                            left_index = True,
                                            right_index = True)
#std_data_final
std_data_final = std_data_final.merge(right = std_data,
                                      how = "left", 
                                      left_index = True,
                                      right_index = True)
std_data_final = std_data_final.merge(right = data_quality_true,
                                      how = "left",
                                      left_index = True,
                                      right_index = True)


# In[ ]:


'''
#51.Outlier處理

dropindex = [387, 1242, 2026, 3360, 3780, 3847]
data_final = data_final.drop(index = dropindex).reset_index(drop = True)
pt_data_final = pt_data_final.drop(index = dropindex).reset_index(drop = True)
minmax_data_final = minmax_data_final.drop(index = dropindex).reset_index(drop = True)
std_data_final = std_data_final.drop(index = dropindex).reset_index(drop = True)
data_outcome = data_outcome.drop(index = dropindex).reset_index(drop = True)
'''


# In[ ]:


#52.分層抽樣
skf = StratifiedKFold(n_splits = 10, shuffle = True, random_state = 10)


# In[ ]:


#53.模型訓練,先切割資料然後再後SMOTE增量


# In[ ]:


#54.Logistic Regression

i = 1
lr_acu_list = []
lr_f1_list = []
lr_roc_list = []
lr_sensitivity_list = []
lr_specificity_list = []
lr_cm_list = []
for lr_train_index, lr_test_index in skf.split(pt_data_final, data_outcome):
    print("{} of kfold {}".format(i, skf.get_n_splits()))
    lr_train_x0, lr_train_y0 = pt_data_final.loc[lr_train_index], data_outcome.loc[lr_train_index]
    lr_test_x, lr_test_y = pt_data_final.loc[lr_test_index], data_outcome.loc[lr_test_index]
    
    lr_train_x1, lr_train_y1 = SMOTE(random_state = 10).fit_resample(lr_train_x0, lr_train_y0)

    
    lr = LogisticRegression(C= 300, 
                            random_state = 10,
                            class_weight = "balanced",
                            max_iter = 5000)
    lr.fit(lr_train_x1, lr_train_y1)
    lr_pred = lr.predict(lr_test_x)
    print("train accuracy: ",lr.score(lr_train_x1, lr_train_y1), "test accuracy: ", lr.score(lr_test_x, lr_test_y))
    print("report:", classification_report(lr_test_y, lr_pred, output_dict = True)["0"]["recall"], classification_report(lr_test_y, lr_pred, output_dict = True)["1"]["recall"])
    lr_acu_score = accuracy_score(lr_test_y, lr_pred)
    lr_f1_score = f1_score(lr_test_y, lr_pred)
    lr_roc_score = roc_auc_score(lr_test_y, lr_pred)
    
    lr_acu_list.append(lr_acu_score)
    lr_f1_list.append(lr_f1_score)
    lr_roc_list.append(lr_roc_score)
    lr_sensitivity_list.append(classification_report(lr_test_y, lr_pred, output_dict = True)["1"]["recall"])
    lr_specificity_list.append(classification_report(lr_test_y, lr_pred, output_dict = True)["0"]["recall"])
    lr_cm_list.append(confusion_matrix(lr_test_y, lr_pred).T)
    print("F1_score", lr_f1_score)
    #sns.heatmap(confusion_matrix(lr_test_y, lr_pred).T, annot = True, square = True, cbar = False, fmt = "d", linewidth = 1)
    i += 1

print("mean acu:", mean(lr_acu_list))
print("mean f1:", mean(lr_f1_list))
print("mean roc:", mean(lr_roc_list))
print("mean sensitivity", mean(lr_sensitivity_list))
print("mean specificity", mean(lr_specificity_list))
sns.set(font_scale = 1.5)
sns.heatmap(confusion_matrix(lr_test_y, lr_pred).T, square = True, annot = True, cbar = False, fmt = "d", linewidths = 1)

lr_summary = pd.DataFrame({"Accuracy": [mean(lr_acu_list)],
                           "F1": [mean(lr_f1_list)],
                           "ROC": [mean(lr_roc_list)],
                           "Sensitivity": [mean(lr_sensitivity_list)],
                           "Specificity": [mean(lr_specificity_list)]})


# In[ ]:


#55.Decision Tree

i = 1
dt_acu_list = []
dt_f1_list = []
dt_roc_list = []
dt_sensitivity_list = []
dt_specificity_list = []
for dt_train_index, dt_test_index in skf.split(data_final, data_outcome):
    print("{} of kfold {}".format(i, skf.get_n_splits()))
    dt_train_x0, dt_train_y0 = data_final.loc[dt_train_index], data_outcome.loc[dt_train_index]
    dt_test_x, dt_test_y = data_final.loc[dt_test_index], data_outcome.loc[dt_test_index]
    
    dt_train_x1, dt_train_y1 = SMOTE(random_state = 10).fit_resample(dt_train_x0, dt_train_y0)
    
    dt = tree.DecisionTreeClassifier(max_depth = 15, 
                                     random_state = 10,
                                     class_weight = "balanced")
    dt.fit(dt_train_x1, dt_train_y1)
    dt_pred = dt.predict(dt_test_x)
    print("train accuracy: ",dt.score(dt_train_x1, dt_train_y1), "test accuracy: ", dt.score(dt_test_x, dt_test_y))
    dt_acu_score = accuracy_score(dt_test_y, dt_pred)
    dt_f1_score = f1_score(dt_test_y, dt_pred)
    dt_roc_score = roc_auc_score(dt_test_y, dt_pred)
    
    dt_acu_list.append(dt_acu_score)
    dt_f1_list.append(dt_f1_score)
    dt_roc_list.append(dt_roc_score)
    dt_specificity_list.append(classification_report(dt_test_y, dt_pred, output_dict = True)["0"]["recall"])
    dt_sensitivity_list.append(classification_report(dt_test_y, dt_pred, output_dict = True)["1"]["recall"])

    

    print("F1_score", dt_f1_score)
    i += 1

print("mean acu:", mean(dt_acu_list))
print("mean f1:", mean(dt_f1_list))
print("mean roc:", mean(dt_roc_list))
print("mean sensitivity", mean(dt_sensitivity_list))
print("mean specificity", mean(dt_specificity_list))

sns.heatmap(confusion_matrix(dt_test_y, dt_pred).T, square = True, annot = True, cbar = False, fmt = "d", linewidths = 1)

dt_summary = pd.DataFrame({"Accuracy": [mean(dt_acu_list)],
                           "F1": [mean(dt_f1_list)],
                           "ROC": [mean(dt_roc_list)],
                           "Sensitivity": [mean(dt_sensitivity_list)],
                           "Specificity": [mean(dt_specificity_list)]})


# In[ ]:


#56.Random forest

i = 1
rf_acu_list = []
rf_f1_list = []
rf_roc_list = []
rf_sensitivity_list = []
rf_specificity_list = []

for rf_train_index, rf_test_index in skf.split(data_final, data_outcome):
    print("{} of kfold {}".format(i, skf.get_n_splits()))
    rf_train_x0, rf_train_y0 = data_final.loc[rf_train_index], data_outcome.loc[rf_train_index]
    rf_test_x, rf_test_y = data_final.loc[rf_test_index], data_outcome.loc[rf_test_index]
    
    rf_train_x1, rf_train_y1 = SMOTE(random_state = 10).fit_sample(rf_train_x0, rf_train_y0)
    
    rf = RandomForestClassifier(random_state = 10,
                                class_weight = "balanced")
    rf.fit(rf_train_x1, rf_train_y1)
    rf_pred = rf.predict(rf_test_x)
    print("train accuracy: ",rf.score(rf_train_x1, rf_train_y1), "test accuracy: ", rf.score(rf_test_x, rf_test_y))
    rf_acu_score = accuracy_score(rf_test_y, rf_pred)
    rf_f1_score = f1_score(rf_test_y, rf_pred)
    rf_roc_score = roc_auc_score(rf_test_y, rf_pred)
    
    rf_acu_list.append(rf_acu_score)
    rf_f1_list.append(rf_f1_score)
    rf_roc_list.append(rf_roc_score)
    rf_specificity_list.append(classification_report(rf_test_y, rf_pred, output_dict = True)["0"]["recall"]) 
    rf_sensitivity_list.append(classification_report(rf_test_y, rf_pred, output_dict = True)["1"]["recall"])

    
    
    print("F1_score", rf_f1_score)
    i += 1
    
print("mean acu:", mean(rf_acu_list))
print("mean f1:", mean(rf_f1_list))
print("mean roc:", mean(rf_roc_list))
print("mean sensitivity", mean(rf_sensitivity_list))
print("mean specificity", mean(rf_specificity_list))
feature_importance = pd.DataFrame({"Feature": data_final.columns,
                                   "Importance": rf.feature_importances_})    
sns.heatmap(confusion_matrix(rf_test_y, rf_pred).T, square = True, annot = True, cbar = False, fmt = "d", linewidths = 1)
rf_summary = pd.DataFrame({"Accuracy": [mean(rf_acu_list)],
                           "F1": [mean(rf_f1_list)],
                           "ROC": [mean(rf_roc_list)],
                           "Sensitivity": [mean(rf_sensitivity_list)],
                           "Specificity": [mean(rf_specificity_list)]})


# In[ ]:


#57.Support vector machine


i = 1
svc_acu_list = []
svc_f1_list = []
svc_roc_list = []
svc_sensitivity_list = []
svc_specificity_list = []
for svc_train_index, svc_test_index in skf.split(minmax_data_final, data_outcome):
    print("{} of Kfold {}".format(i, skf.get_n_splits()))
    svc_train_x0, svc_train_y0 = minmax_data_final.loc[svc_train_index], data_outcome.loc[svc_train_index]
    svc_test_x, svc_test_y = minmax_data_final.loc[svc_test_index], data_outcome.loc[svc_test_index]
    
    svc_train_x1, svc_train_y1 = SMOTE(random_state = 10).fit_sample(svc_train_x0, svc_train_y0)
    
    svc = SVC(random_state = 10)
    svc.fit(svc_train_x1, svc_train_y1)
    svc_pred = svc.predict(svc_test_x)
    print("train accuracy: ",svc.score(svc_train_x1, svc_train_y1), "test accuracy: ", svc.score(svc_test_x, svc_test_y))
    svc_acu_score = accuracy_score(svc_test_y, svc_pred)
    svc_f1_score = f1_score(svc_test_y, svc_pred)
    svc_roc_score = roc_auc_score(svc_test_y, svc_pred)
    
    svc_acu_list.append(svc_acu_score)
    svc_f1_list.append(svc_f1_score)
    svc_roc_list.append(svc_roc_score)
    svc_specificity_list.append(classification_report(svc_test_y, svc_pred, output_dict = True)["0"]["recall"]) 
    svc_sensitivity_list.append(classification_report(svc_test_y, svc_pred, output_dict = True)["1"]["recall"])
    print("F1_score", svc_f1_score)
    i += 1
    
print("mean acu:", mean(svc_acu_list))
print("mean f1:", mean(svc_f1_list))
print("mean roc:", mean(svc_roc_list))
print("mean sensitivity", mean(svc_sensitivity_list))
print("mean specificity", mean(svc_specificity_list))

sns.set(font_scale = 1.5)
sns.heatmap(confusion_matrix(svc_test_y, svc_pred), annot = True, square = True, cbar = False, fmt = "d", linewidths = 1)
svc_summary = pd.DataFrame({"Accuracy": [mean(svc_acu_list)],
                           "F1": [mean(svc_f1_list)],
                           "ROC": [mean(svc_roc_list)],
                           "Sensitivity": [mean(svc_sensitivity_list)],
                           "Specificity": [mean(svc_specificity_list)]})


# In[ ]:


#58.XGBoost

i = 1
xgb_acu_list = []
xgb_f1_list = []
xgb_roc_list = []
xgb_sensitivity_list = []
xgb_specificity_list = []

for xgb_train_index, xgb_test_index in skf.split(data_final, data_outcome):
    print("{} of kfold {}".format(i, skf.get_n_splits()))
    xgb_train_x0, xgb_train_y0 = data_final.loc[xgb_train_index], data_outcome.loc[xgb_train_index]
    xgb_test_x, xgb_test_y = data_final.loc[xgb_test_index], data_outcome.loc[xgb_test_index]
    
    xgb_train_x1, xgb_train_y1 = SMOTE(random_state = 10).fit_sample(xgb_train_x0, xgb_train_y0)
    
    
    xgb_train_x2 = pd.DataFrame(xgb_train_x1, columns = xgb_test_x.columns)
    xgb_train_y2 = pd.DataFrame(xgb_train_y1, columns = [xgb_test_y.name])
    
    xgb = XGB.XGBClassifier(n_estimators = 100, random_state = 10)
    xgb.fit(xgb_train_x2, xgb_train_y2)
    xgb_pred = xgb.predict(xgb_test_x)
    print("train accuracy: ",xgb.score(xgb_train_x2, xgb_train_y2), "test accuracy: ", xgb.score(xgb_test_x, xgb_test_y))
    xgb_acu_score = accuracy_score(xgb_test_y, xgb_pred)
    xgb_f1_score = f1_score(xgb_test_y, xgb_pred)
    xgb_roc_score = roc_auc_score(xgb_test_y, xgb_pred)
    
    xgb_acu_list.append(xgb_acu_score)
    xgb_f1_list.append(xgb_f1_score)
    xgb_roc_list.append(xgb_roc_score)
    xgb_specificity_list.append(classification_report(xgb_test_y, xgb_pred, output_dict = True)["0"]["recall"]) 
    xgb_sensitivity_list.append(classification_report(xgb_test_y, xgb_pred, output_dict = True)["1"]["recall"])
    
    print("f1score", xgb_f1_score)
    i += 1

print("mean acu:", mean(xgb_acu_list))
print("mean f1:", mean(xgb_f1_list))
print("mean roc:", mean(xgb_roc_list))
print("mean sensitivity", mean(xgb_sensitivity_list))
print("mean specificity", mean(xgb_specificity_list))
sns.heatmap(confusion_matrix(xgb_test_y, xgb_pred).T, annot = True, square = True, cbar = False, fmt = "d", linewidths = 1)
xgb_summary = pd.DataFrame({"Accuracy": [mean(xgb_acu_list)],
                           "F1": [mean(xgb_f1_list)],
                           "ROC": [mean(xgb_roc_list)],
                           "Sensitivity": [mean(xgb_sensitivity_list)],
                           "Specificity": [mean(xgb_specificity_list)]})


# In[ ]:


#59.Mutiple Layer Perceptron


i = 1
mlp_acu_list = []
mlp_f1_list = []
mlp_roc_list = []
mlp_sensitivity_list = []
mlp_specificity_list = []
for mlp_train_index, mlp_test_index in skf.split(std_data_final, data_outcome):
    print("{} of kfold {}".format(i, skf.get_n_splits()))
    mlp_train_x0, mlp_train_y0 = std_data_final.loc[mlp_train_index], data_outcome.loc[mlp_train_index]
    mlp_test_x, mlp_test_y = std_data_final.loc[mlp_test_index], data_outcome.loc[mlp_test_index]
    
    mlp_train_x1, mlp_train_y1 = SMOTE(random_state = 10).fit_sample(mlp_train_x0, mlp_train_y0)
    
    mlp = MLPClassifier((100, 100, 100), random_state = 10)
    mlp.fit(mlp_train_x1, mlp_train_y1)
    mlp_pred = mlp.predict(mlp_test_x)
    print("train accuracy: ",mlp.score(mlp_train_x1, mlp_train_y1), "test accuracy: ", mlp.score(mlp_test_x, mlp_test_y))
    mlp_acu_score = accuracy_score(mlp_test_y, mlp_pred)
    mlp_f1_score = f1_score(mlp_test_y, mlp_pred)
    mlp_roc_score = roc_auc_score(mlp_test_y, mlp_pred)
    
    mlp_acu_list.append(mlp_acu_score)
    mlp_f1_list.append(mlp_f1_score)
    mlp_roc_list.append(mlp_roc_score)
    mlp_specificity_list.append(classification_report(mlp_test_y, mlp_pred, output_dict = True)["0"]["recall"]) 
    mlp_sensitivity_list.append(classification_report(mlp_test_y, mlp_pred, output_dict = True)["1"]["recall"])
    

    print("f1score", mlp_f1_score)
    i += 1

print("mean acu:", mean(mlp_acu_list))
print("mean f1:", mean(mlp_f1_list))
print("mean roc:", mean(mlp_roc_list))
print("mean sensitivity", mean(mlp_sensitivity_list))
print("mean specificity", mean(mlp_specificity_list))   
sns.heatmap(confusion_matrix(mlp_test_y, mlp_pred).T, annot = True, square = True, cbar = False, fmt = "d", linewidths = 1)
mlp_summary = pd.DataFrame({"Accuracy": [mean(mlp_acu_list)],
                           "F1": [mean(mlp_f1_list)],
                           "ROC": [mean(mlp_roc_list)],
                           "Sensitivity": [mean(mlp_sensitivity_list)],
                           "Specificity": [mean(mlp_specificity_list)]})


# In[ ]:


#60.Naive-bayes

i = 1
gnb_acu_list = []
gnb_f1_list = []
gnb_roc_list = []
gnb_sensitivity_list = []
gnb_specificity_list = []
for gnb_train_index, gnb_test_index in skf.split(pt_data_final, data_outcome):
    print("{} of kfold {}".format(i, skf.get_n_splits()))
    gnb_train_x0, gnb_train_y0 = pt_data_final.loc[gnb_train_index], data_outcome.loc[gnb_train_index]
    gnb_test_x, gnb_test_y = pt_data_final.loc[gnb_test_index], data_outcome.loc[gnb_test_index]
    
    gnb_train_x1, gnb_train_y1 = SMOTE(random_state = 10).fit_sample(gnb_train_x0, gnb_train_y0)
    
    gnb = GaussianNB()
    gnb.fit(gnb_train_x1, gnb_train_y1)
    gnb_pred = gnb.predict(gnb_test_x)
    print("train accuracy: ",gnb.score(gnb_train_x1, gnb_train_y1), "test accuracy: ", gnb.score(gnb_test_x, gnb_test_y))
    gnb_acu_score = accuracy_score(gnb_test_y, gnb_pred)
    gnb_f1_score = f1_score(gnb_test_y, gnb_pred)
    gnb_roc_score = roc_auc_score(gnb_test_y, gnb_pred)
    
    gnb_acu_list.append(gnb_acu_score)
    gnb_f1_list.append(gnb_f1_score)
    gnb_roc_list.append(gnb_roc_score)
    gnb_specificity_list.append(classification_report(gnb_test_y, gnb_pred, output_dict = True)["0"]["recall"]) 
    gnb_sensitivity_list.append(classification_report(gnb_test_y, gnb_pred, output_dict = True)["1"]["recall"])

    print("f1score", gnb_f1_score)
    i += 1
print("mean acu:", mean(gnb_acu_list))
print("mean f1:", mean(gnb_f1_list))
print("mean roc:", mean(gnb_roc_list))
print("mean sensitivity", mean(gnb_sensitivity_list))
print("mean specificity", mean(gnb_specificity_list)) 
sns.heatmap(confusion_matrix(gnb_test_y, gnb_pred).T, annot = True, square = True, cbar = False, fmt = "d", linewidths = 1)
gnb_summary = pd.DataFrame({"Accuracy": [mean(gnb_acu_list)],
                           "F1": [mean(gnb_f1_list)],
                           "ROC": [mean(gnb_roc_list)],
                           "Sensitivity": [mean(gnb_sensitivity_list)],
                           "Specificity": [mean(gnb_specificity_list)]})


# In[ ]:


#61.模型評估

f1 = list([max(lr_f1_list),
          max(dt_f1_list),
          max(rf_f1_list), 
          max(svc_f1_list),
          max(xgb_f1_list),
          max(mlp_f1_list),
          max(gnb_f1_list)])
Model = ["Logistic Regression", 
         "Decision Tree", 
         "Random Forest", 
         "Support Vector Machine", 
         "XGBoost", 
         "Mutiple layer Perceptron", 
         "GaussianNB"]
f1scoreplot = pd.DataFrame({"f1": f1, 
                            "Model": Model}).sort_values("f1")
plt.barh(y = f1scoreplot["Model"],
         width = f1scoreplot["f1"])


# In[ ]:


#62.F1-score
index_list_f1 = ["Logistic_Regression", 
                 "Decision_Tree", 
                 "Random_Forest", 
                 "SVM", 
                 "XGBoost", 
                 "Mutiple layer Perceptron", 
                 "GaussianNB"]
mean_list_f1 = [mean(lr_f1_list),
                mean(dt_f1_list),
                mean(rf_f1_list),
                mean(svc_f1_list),
                mean(xgb_f1_list),
                mean(mlp_f1_list),
                mean(gnb_f1_list)]
mean_f1 = pd.DataFrame(data = mean_list_f1,
                       index = index_list_f1,
                       columns = ["F1_score"]
                       )


# In[ ]:


#63.AUC 
index_list_auc = ["Logistic_Regression", 
                  "Decision_Tree", 
                  "Random_Forest", 
                  "SVM", 
                  "XGBoost", 
                  "Mutiple layer Perceptron", 
                  "GaussianNB"]
mean_list_roc = [mean(lr_roc_list),
                 mean(dt_roc_list),
                 mean(rf_roc_list),
                 mean(svc_roc_list),
                 mean(xgb_roc_list),
                 mean(mlp_roc_list),
                 mean(gnb_roc_list)]
mean_roc = pd.DataFrame(data = mean_list_roc,
                        index = index_list_auc, 
                        columns = ["ROC_score"]
                        )


# In[ ]:


#64.acu
index_list_acu = ["Logistic_Regression",
                  "Decision_Tree",
                  "Random_Forest",
                  "SVM",
                  "XGBoost",
                  "Multiple Layer Perceptron",
                  "GaussianNB"]
mean_list_acu = [mean(lr_acu_list),
                 mean(dt_acu_list),
                 mean(rf_acu_list),
                 mean(svc_acu_list),
                 mean(xgb_acu_list),
                 mean(mlp_acu_list),
                 mean(gnb_acu_list),]
mean_acu = pd.DataFrame(data = mean_list_acu,
                        index = index_list_acu,
                        columns = ["Accuracy"])


# In[ ]:


#65.sensitivity
index_list_sensitivity = ["Logistic_Regression",
                          "Decision_Tree",
                          "Random_Forest",
                          "SVM",
                          "XGBoost",
                          "Multiple Layer Perceptron",
                          "GaussianNB"]
mean_list_sensitivity = [mean(lr_sensitivity_list),
                         mean(dt_sensitivity_list),
                         mean(rf_sensitivity_list),
                         mean(svc_sensitivity_list),
                         mean(xgb_sensitivity_list),
                         mean(mlp_sensitivity_list),
                         mean(gnb_sensitivity_list)]
mean_sensitivity = pd.DataFrame(data = mean_list_sensitivity,
                                index = index_list_sensitivity,
                                columns = ["Sentivity"])


# In[ ]:


#66.specificity
index_list_specificity = ["Logistic_Regression",
                          "Decision_Tree",
                          "Random_Forest",
                          "SVM",
                          "XGBoost",
                          "Multiple Layer Perceptron",
                          "GaussianNB"]
mean_list_specificity = [mean(lr_specificity_list),
                         mean(dt_specificity_list),
                         mean(rf_specificity_list),
                         mean(svc_specificity_list),
                         mean(xgb_specificity_list),
                         mean(mlp_specificity_list),
                         mean(gnb_specificity_list)]
mean_specificity = pd.DataFrame(data = mean_list_specificity,
                                index = index_list_specificity,
                                columns = ["Specificity"])

