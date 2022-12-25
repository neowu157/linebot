# linebot

## 前言
接近大四,即將收到體檢兵單，很多男生會很想知道自己的bmi與自己的兵役體位,這個bot可以幫助到他們。

## 構想
使用者輸入的性別、身高、體重、linebot會回傳bmi與體位

## 環境
- windows 11
- anaconda
- pychram
- python 3.9

## 使用教學
1. 透過anaconda打開pycharm

2. 讓pycharm安裝所需套件

3. 從`.env.sample`產生出一個`.env`，並填入以下資訊

- Line
    - LINE_CHANNEL_SECRET
    - LINE_CHANNEL_ACCESS_TOKEN
    
4.下載windows版ngrok

3.執行ngrok.exe
```shell
ngrok http 8000
```
6. execute app.py
```shell
py app.py
```


## 使用說明
- 基本操作
    - 所有用到英文的指令大小寫皆可
    - 隨時輸入任何字若沒觸發到都會有提示
    - 以下二個指令皆可隨時輸入
        - `restart`
            - reset所有資訊
        - `fsm`
            - 傳回當前的fsm圖片
- 架構圖
    1. 輸入`bmi`開始使用小幫手
    2. 輸入性別 -> `男生`或`女生`
    3. 輸入身高 -> `整數`
    4. 輸入體重 -> `整數`
    5. bot回傳體位與bmi
    


## FSM
![](https://i.imgur.com/t8CxmXp.png)
### state說明
- user: 輸入bmi開始使用健身小幫手
- input_gender: 輸入男生或女生
- input_height: 輸入身高(整數)
- input_weight: 輸入體重(整數)
- show_result:  bot輸出兵役體位及BMI
