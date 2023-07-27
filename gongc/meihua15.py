import streamlit as st
import pandas as pd
import time
from PIL import Image
import datetime
from streamlit.components.v1 import html
# from sklearn.metrics import confusion_matrix, roc_auc_score


js_code = '''
$(document).ready(function(){
    $("div[data-testid=stToolbar]", window.parent.document).remove()
});
'''
# 因为JS不需要展示，所以html宽高均设为0，避免占用空间，且放置在所有组件最后
# 引用了JQuery v2.2.4
html(f'''<script src="https://cdn.bootcdn.net/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
    <script>{js_code}</script>''',
     width=0,
     height=0)
# def dat(data):
#     data_k = data.reset_index()
#     try:
#         aa = roc_auc_score(data_k['label'],data_k['proba'])
#     except:
#         aa = None
#     return aa

tab1, tab2 = st.tabs(["性别预测", "疾病预测"])

with tab1:

    st.markdown(
        """
        ## 性别预测作业系统
        ###
        """
    )
    st.markdown(
        """
        #### 提交作业
        """
    )


    now = datetime.datetime.now().replace(microsecond=0)+ datetime.timedelta(hours=8)
    df = pd.read_csv('./gongc/test_label.csv')
    data = pd.read_csv('./gongc/111.csv')
    # label_t = df['gender']
    # 创建file_uploader组件
    uploaded_file = st.file_uploader("请依据示例文件提交csv文件，命名需使用自己的姓名", type={"csv", "txt"},key ='1')
    if uploaded_file is not None:
        try:
            spectra = pd.read_csv(uploaded_file)
            # spectra.columns = ['user_id', 'coupon_id', 'date_received', 'proba']
            start_message = st.empty()
            time.sleep(0.5)
            start_message.caption('提交成功，正在评估中，请等待一段时间!!!:coffee::coffee::coffee:')
            if (df['user_id'] == spectra['user_id']).sum() == len(df):
                spectra['label'] = df['gender']
                sc = (spectra['label'] == spectra['gender']).mean()
                # sc = spectra[['coupon_id', 'proba', 'label']].groupby('coupon_id').apply(dat).mean()
                time.sleep(1.5)
                start_message.caption('评估完成!!!:blossom::blossom::blossom:')
                time.sleep(2)
                start_message.empty()
                st.balloons()
            else:
                sc = 0.5
                time.sleep(3)
                start_message.error('提交错误，请注意提交格式', icon="🚨")
                time.sleep(3)
                start_message.empty()

            name = uploaded_file.name.split('.')[0]
            # st.write(name)
            st.write('准确率：', round(sc,2))
            # st.write('排名为：')
            data1 = {'name': [name], 'score': [round(sc,2)], 's_time': [now]}
            data1 = pd.DataFrame(data1)
            data = pd.concat([data, data1])
            data['s_time'] = pd.to_datetime(data['s_time'])
            # data['score'] = round(data['score'],2)
            data = data.sort_values(by=['score', 's_time'], ascending=[False, True])
            data = data.reset_index(drop=True)
            data = data.drop_duplicates(subset='name',keep = 'first')
            # st.write(data)
            data.to_csv('./gongc/111.csv', index=False)
            data['rank'] = data['score'].rank(method='min',ascending=False)
            st.write('排名为：',int(data[(data['name'] == name)]['rank'].values))



        except:
            st.error('导入文件不规范，请按照示例文件格式修改后再进行上传文件', icon="🚨")
            image = Image.open('./gongc/ces.png')
            st.image(image, caption='请查看示例文件')

        with st.expander("查看排行榜"):
            st.write(data)


            def convert_df(df):
                return df.to_csv().encode('utf-8')


            csv = convert_df(data)
            st.download_button(
                label='下载排行榜',
                data=csv,
                file_name='排行榜数据1.csv',
                key='14'
            )

with tab2:
   # st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
   st.markdown(
       """
       ## 疾病预测作业系统
       ###
       """
   )
   st.markdown(
       """
       #### 提交作业
       """
   )

   now = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(hours=8)
   df = pd.read_csv('./gongc/AD_CN_label.csv')
   data = pd.read_csv('./gongc/222.csv')
   label_t = df['label']
   # 创建file_uploader组件
   uploaded_file = st.file_uploader("请依据示例文件提交csv文件，命名需使用自己的姓名", type={"csv", "txt"},key ='2')
   if uploaded_file is not None:
       try:
           spectra = pd.read_csv(uploaded_file)
           # spectra.columns = ['user_id', 'coupon_id', 'date_received', 'proba']
           start_message = st.empty()
           time.sleep(0.5)
           start_message.caption('提交成功，正在评估中，请等待一段时间!!!:coffee::coffee::coffee:')
           if (df['name'] == spectra['name']).sum() == len(df):
               spectra['gender'] = df['label']
               sc = (spectra['label'] == spectra['gender']).mean()
               # sc = spectra[['coupon_id', 'proba', 'label']].groupby('coupon_id').apply(dat).mean()
               time.sleep(1.5)
               start_message.caption('评估完成!!!:blossom::blossom::blossom:')
               time.sleep(2)
               start_message.empty()
               st.balloons()
           else:
               sc = 0.5
               time.sleep(3)
               start_message.error('提交错误，请注意提交格式', icon="🚨")
               time.sleep(3)
               start_message.empty()

           name = uploaded_file.name.split('.')[0]
           # st.write(name)
           st.write('准确率：', round(sc, 2))
           # st.write('排名为：')
           data1 = {'name': [name], 'score': [round(sc, 2)], 's_time': [now]}
           data1 = pd.DataFrame(data1)
           data = pd.concat([data, data1])
           data['s_time'] = pd.to_datetime(data['s_time'])
           # data['score'] = round(data['score'],2)
           data = data.sort_values(by=['score', 's_time'], ascending=[False, True])
           data = data.reset_index(drop=True)
           data = data.drop_duplicates(subset='name', keep='first')
           # st.write(data)
           data.to_csv('./gongc/222.csv', index=False)
           data['rank'] = data['score'].rank(method='min', ascending=False)
           st.write('排名为：', int(data[(data['name'] == name)]['rank'].values))

       except:
           st.error('导入文件不规范，请按照下面的例子再进行上传文件', icon="🚨")
           image = Image.open('./gongc/ces2.png')
           st.image(image, caption='请查看示例文件')
       with st.expander("查看排行榜"):
           st.write(data)


           def convert_df(df):
               return df.to_csv().encode('utf-8')


           csv = convert_df(data)
           st.download_button(
               label='下载排行榜',
               data=csv,
               file_name='排行榜数据2.csv',
               key='13'
           )

# with tab3:
#
#    # st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
#    # st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
#    st.markdown(
#        """
#        ## 电商客流量预测作业系统
#        ###
#        """
#    )
#    st.markdown(
#        """
#        #### 提交作业
#        """
#    )
#
#    now = datetime.datetime.now().replace(microsecond=0) + datetime.timedelta(hours=8)
#    df = pd.read_csv('./gongc/sc3.csv')
#    data = pd.read_csv('./gongc/333.csv')
#    label_t = df['label']
#    # 创建file_uploader组件
#    uploaded_file = st.file_uploader("请提交仅含[label]列的csv文件，命名需使用自己的姓名", type={"csv", "txt"}, key='3')
#    if uploaded_file is not None:
#        try:
#            spectra = pd.read_csv(uploaded_file)
#            label_p = spectra['label']
#            sc = sum(label_t == label_p) / len(label_t)
#            name = uploaded_file.name.split('.')[0]
#            # st.write(name)
#            st.write('准确度为：', round(sc,2))
#            # st.write('排名为：')
#            data1 = {'name': [name], 'score': [sc], 's_time': [now]}
#            data1 = pd.DataFrame(data1)
#            data = pd.concat([data, data1])
#            data['s_time'] = pd.to_datetime(data['s_time'])
#            data['score'] = round(data['score'], 2)
#            data = data.sort_values(by=['score', 's_time'], ascending=[False, True])
#            data = data.reset_index(drop=True)
#            data = data.drop_duplicates(subset='name', keep='first')
#            # st.write(data)
#            data.to_csv('./gongc/333.csv', index=False)
#            data['rank'] = data['score'].rank(method='min', ascending=False)
#            st.write('排名为：', int(data[(data['name'] == name)]['rank'].values))
#            st.balloons()
#
#
#        except:
#            st.error('导入文件不规范，请按照下面的例子再进行上传文件', icon="🚨")
#            image = Image.open('./gongc/ces.jpg')
#            st.image(image, caption='仅有一列label的csv文件')
#        with st.expander("查看排行榜"):
#            st.write(data)
#
#
#            def convert_df(df):
#                return df.to_csv().encode('utf-8')
#
#
#            csv = convert_df(data)
#            st.download_button(
#                label='下载排行榜',
#                data=csv,
#                file_name='排行榜数据.csv',
#                key = '12'
#            )
