import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import time
import plotly.figure_factory as ff
import pandas as pd

# st.set_page_config(layout="wide")

with st.sidebar:
    selected = option_menu("Main Menu", ["add knowledge domain/subject", 'view knowledge domain/subject','add organization','genrate plan','add rating'], 
        icons=['add', 'list-task','list-task','list-task'], menu_icon="cast", default_index=0)

if selected =="add knowledge domain/subject":
    st.title("add knowledge domain/subject")
    st.markdown("""---""")
    st.subheader('add knowledge domain:')
    knowledge = st.text_input("enter knowledge domain name:")
    st.subheader('add knowledge domain prerequisite')
    st.caption('type (any) for no prerequisite and for  multi prerequisite split by - .' )
    st.caption('age must input range like 1-5.' )
    col1, col2= st.columns(2)
    
    with col1:
        degree = st.text_input('degree:')
        jop = st.text_input('jop:')
        age = st.text_input('age:')
    with col2:
        adminstration = st.text_input('adminstration:')
        organization = st.text_input('organization:')
        oldcourse = st.text_input('old course')
        
    if st.button("add knowledge domain") and knowledge and degree and jop and age and adminstration and organization and oldcourse:
        con = sqlite3.connect("data_store.db")                   
        cur = con.cursor()
        con.execute("create table if not exists knowledge  (id INTEGER PRIMARY KEY AUTOINCREMENT, knowledgename TEXT NOT NULL, degree TEXT NOT NULL, jop TEXT NOT NULL , age TEXT NOT NULL , administration TEXT NOT NULL , organization TEXT NOT NULL, oldcourse TEXT NOT NULL)")
        with sqlite3.connect("data_store.db") as con:  
            cur = con.cursor()  
            cur.execute("INSERT into knowledge (knowledgename, degree, jop,age,administration,organization,oldcourse) values (?,?,?,?,?,?,?)",(knowledge,degree,jop,age,adminstration,organization,oldcourse))  
            con.commit()
            
        with st.empty():
            for seconds in range(3):
                st.write(f"⏳ {seconds} seconds have passed")
                time.sleep(1)
            st.write("✔️ saved!")  
            
    st.markdown("""---""")
    st.subheader('add subject (courese):')
    
    con = sqlite3.connect("data_store.db") 
    cur = con.cursor()

    cur.execute("select id, knowledgename  from knowledge  ;")
    result = cur.fetchall()
    modules = []
    for i in result:
        modules.append(str(i[1]))
    option = st.selectbox(
    'selecte knowledge domain:',modules)
    
    subjectName=st.text_input('subject name:')
    col1, col2= st.columns(2)
    
    with col1:
        typ = st.radio("Study method :",['any',"online", "off line"] , horizontal=True)
        joplevel = st.text_input('jop level:')
        ageRange = st.text_input('age range:')
    with col2:
        degree = st.text_input('degree: ')
        courseHouer = st.text_input('course Houer:')
        oldcourse = st.text_input('old course:')
    if st.button("add subject"):
        if option and subjectName:
            con = sqlite3.connect("data_store.db")                   
            cur = con.cursor()
            con.execute("create table if not exists subject  (id INTEGER PRIMARY KEY AUTOINCREMENT, subjectName TEXT NOT NULL, knowledgename TEXT NOT NULL, typeS TEXT NOT NULL ,joplevel TEXT NOT NULL , ageRange TEXT NOT NULL , degree TEXT NOT NULL , courseHouer TEXT NOT NULL ,oldcourse TEXT NOT NULL)")
            with sqlite3.connect("data_store.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into subject (subjectName, knowledgename ,typeS ,joplevel ,ageRange ,degree,courseHouer ,oldcourse) values (?,?,?,?,?,?,?,?)",(subjectName,option,typ,joplevel,ageRange,degree,courseHouer,oldcourse))  
                con.commit()
            with st.empty():
                for seconds in range(3):
                    st.write(f"⏳ {seconds} seconds have passed")
                    time.sleep(1)
                st.write("✔️ saved!")
    
    con = sqlite3.connect("data_store.db") 
    cur = con.cursor()

    cur.execute("select *  from subject  ;")
    result = cur.fetchall()
    if result:
        data_matrix = []
        data_matrix.append(['#','subject','knowledge domain'])
        for i in result:
            data_matrix.append([i[0],i[1],i[2]])
        fig = ff.create_table(data_matrix)
            
        st.plotly_chart(fig)
    
if selected =="view knowledge domain/subject":
    st.title("view  knowledge domain/subject")
    st.markdown("""---""")
    con = sqlite3.connect("data_store.db") 
    cur = con.cursor()

    subject = cur.execute("select *  from subject  ;")
    subject = subject.fetchall()
    module = cur.execute("select *  from knowledge  ;")
    module = module.fetchall()
    for mod in module:
        st.subheader(mod[1])
        st.write('prerequisite:')
        col1, col2= st.columns(2)
        
        with col1:
            st.write('degree: '+str(mod[2]))
            st.write('jop: '+str(mod[3]))
            st.write('age: '+str(mod[4]))
        with col2:
            st.write('adminstration: '+str(mod[5]))
            st.write('organization: '+str(mod[6]))
            st.write('old course: '+str(mod[7]))
        st.write('subject:')    
        for sub in subject:
            if sub[2] == mod[1]:
                st.text(sub[1] + " with prerequisite " +sub[8] + " and type of stude "+ sub[3] )
        st.markdown("""---""")         
if selected == 'add organization':
    st.subheader('add organization')
    organizatin = st.text_input('organizatin:')
    if st.button("add") :
        con = sqlite3.connect("data_store.db")                   
        cur = con.cursor()
        con.execute("create table if not exists organization  (id INTEGER PRIMARY KEY AUTOINCREMENT, organizationName TEXT NOT NULL)")
        with sqlite3.connect("data_store.db") as con:  
            cur = con.cursor()  
            cur.execute("INSERT into organization (organizationName) values (?)",([organizatin]))  
            con.commit()
        with st.empty():
            for seconds in range(3):
                st.write(f"⏳ {seconds} seconds have passed")
                time.sleep(1)
            st.write("✔️ add!")
    
    con = sqlite3.connect("data_store.db") 
    cur = con.cursor()

    org = cur.execute("select *  from organization  ;")
    org = org.fetchall()
    
    for mod in org:
        
        st.write(mod[1])
    
    
if selected =="genrate plan":
    
    con = sqlite3.connect("data_store.db") 
    cur = con.cursor()

    org = cur.execute("select *  from organization  ;")
    org = org.fetchall()
    orgainzation =[]
    for mod in org:
        orgainzation.append(mod[1])
     
    col1, col2= st.columns(2)
    with col1:
        org = st.selectbox('organization: ',orgainzation) 
        administration = st.text_input('administration') 
        job = st.text_input('job:')
        
    with col2:
        degree = st.text_input('degree:')
        age = st.text_input('age:')
        oldCourse = st.text_input('old subject (course):')
        
     
    st.caption('old subject (course) must separeted with (-) .')   
    active = st.checkbox('custum plan')
    
    con = sqlite3.connect("data_store.db") 
    cur = con.cursor()

    org = cur.execute("select *  from subject  ;")
    org = org.fetchall()
    subject =[]
    for mod in org:
        subject.append(mod[1])
    subj = st.multiselect('select custum subject: ',subject,disabled = (not active))
    for sub in org:
        if  sub[1] in subj  :
            if 'any' in sub[8] :
                st.success('allowed', icon="✅")
                st.write(sub[2])
                st.write('course :blue['+sub[1]+'] ' +'with '+sub[7] +' H')
            else:
                st.warning('prerequisite needed', icon="⚠️")
                st.write(sub[2])
                st.write('course :blue['+sub[1]+'] ' +'with '+sub[7] +' H')
                st.write(':red[prerequisite] needed is : ' + sub[8])
                
    if st.button("genrate") :
        con = sqlite3.connect("data_store.db") 
        cur = con.cursor()

        cur.execute("select *  from knowledge  ;")
        result = cur.fetchall()
        plan = []
        for i in result:
            if (org in i[6] or 'any'in i[6]) and (administration in i[5] or 'any'in i[5]) and (job in i[3] or 'any'in i[3]) and (degree in i[2] or 'any'in i[2]) and ((age >= i[4].split('-')[0] and age <= i[4].split('-')[1] ) or 'any'in i[4]) and (set(oldCourse.split('-')).issubset(set(i[7].split('-'))) or 'any'in i[7]):
                
                
                
                subject = cur.execute("select *  from subject  ;")
                subject = subject.fetchall()
                st.subheader("Recommended knowledge domain: "+i[1])
                st.write("subject:")
                for sub in subject:
                    if sub[2] == i[1]:
                        if 'any' in sub[8] or set(oldCourse.split('-')).issubset(set(sub[8].split('-')))  :
                            st.write('course :blue['+sub[1]+'] ' +'with '+sub[7] +' H')
                        else:
                            st.write('course :blue['+sub[1] +']'+'with '+sub[7] +' H'+' need :red['+ sub[8] +'] first')
        st.toast('plane genrated!', icon='🎉')
        
    uploaded_file = st.file_uploader("upload trainee data")
    if uploaded_file is not None:
        dfUpload = pd.read_excel(uploaded_file)
    
    
    