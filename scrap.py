from ast import Break
from selenium import webdriver
import time
from random import randint
import pandas as pd

int_txt = 1
caracter_comillas = "'"

mail_password =[['linkediiiiiiiiin12@gmail.com','uno23456789'],['random1234usos@gmail.com','uno23456789']]
array_ids = ["about", "courses", "experience", "education", "licenses_and_certifications", "skills", "languages", "recommendations", "final"]

condicion = True
data_key ={
    'Details':[],
    'About':[],
    'Courses':[],
    'Experience':[],
    'Education':[],
    'Licenses and certifications':[],
    'Skills':[],
    'Languages':[],
    'Recommendations':[]
}

for i in mail_password:

    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get("https://www.linkedin.com/login/es?trk=homepage-basic_ispen-login-button")
    time.sleep(5)

    try:
        driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[1]/input').send_keys(i[0])
        driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[2]/input').send_keys(i[1])
        driver.find_element_by_xpath('/html/body/div/main/div[2]/div[1]/form/div[3]/button').click()

    except:
        driver.find_element_by_xpath('/html/body/main/section[1]/div/div/form/div[2]/div[1]/input').send_keys(i[0])
        driver.find_element_by_xpath('/html/body/main/section[1]/div/div/form/div[2]/div[2]/input').send_keys(i[1])
        driver.find_element_by_xpath('/html/body/main/section[1]/div/div/form/button').click()

    AUX_INPUT = input('Apreta para continuar')

    Lecture = open('Links_'+str(int_txt)+'.txt','r')
    cont_profiles = 0

    for link_profile in Lecture.readlines():

        cont=1

        profile = []

        driver.get(link_profile)
        time.sleep(2)

        data_basic = []
        int_div_main = 5

        name = ''
        work = ''
        location = ''
    
        try:
            while(True):

                try:
                    name = driver.find_element_by_xpath('/html/body/div['+str(int_div_main)+']/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/h1').text
                    work = driver.find_element_by_xpath('/html/body/div['+str(int_div_main)+']/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]').text
                    location = driver.find_element_by_xpath('/html/body/div['+str(int_div_main)+']/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[1]').text

                    x_path_general = '/html/body/div['+str(int_div_main)+']/div[3]/div/div/div[2]/div/div/main/'

                    data_basic.append(name)
                    data_basic.append(work)
                    data_basic.append(location)

                    #indice 0 de profile: nombre, trabajo, locacion
                    profile.append(data_basic)
                    break     

                except:
                    int_div_main+=1

                if(int_div_main>6):
                    break

            for id in array_ids:

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                if(id=="final"):
                    break

                #para corroborar que el div cambia al volver al perfil, sino lo cambia por otro n??mero

                try:
                    name_aux = driver.find_element_by_xpath('/html/body/div['+str(int_div_main)+']/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/h1').text

                    if(name==name_aux):
                        condition = True

                except:
                    condition = False

                if(condition==True):
                    x_path_general = x_path_general

                else:
                    if(int_div_main==5):
                        int_div_main=6
                    else:
                        int_div_main=5

                    x_path_general = '/html/body/div['+str(int_div_main)+']/div[3]/div/div/div[2]/div/div/main/'
                
                int_section = 1

                while(True):
                    try:
                        driver.find_element_by_xpath(x_path_general+"/section["+str(int_section)+"]/div[@id="+caracter_comillas+id+caracter_comillas+"]")
                        x_path_actual = x_path_general+"/section["+str(int_section)+"]"
                        
                        if(id=="about"):
                            
                            try:
                                about_profile = driver.find_element_by_xpath(x_path_actual+"/div[3]/div/div/div/span[1]").text
                                profile.append([about_profile])
                                break

                            except:
                                profile.append(float('NaN'))
                                break

                        if(id=="courses"):


                            courses = []
                            int_course = 1

                            try:
                                #con boton
                                see_more_courses_link = driver.find_element_by_xpath(x_path_actual+'/div[3]/div/a').get_attribute('href')
                                driver.get(see_more_courses_link)
                                time.sleep(3)

                                x_path_general_aux = '/html/body/div['+str(int_div_main)+']/div[3]/div/div/div[2]/div/div/main/'

                                while(True):

                                    try:
                                        try:
                                            course = driver.find_element_by_xpath(x_path_general_aux+'/section/div[2]/div/div[1]/ul/li['+str(int_course)+']/div/div[2]/div[1]/div[1]/div/span/span[1]').text
                                            courses.append(course)
                                            int_course+=1
                                        except:
                                            break

                                    except:
                                        if(int_div_main==5):
                                            int_div_main=6

                                        else:
                                            int_div_main=5

                                        x_path_general_aux = '/html/body/div['+str(int_div_main)+']/div[3]/div/div/div[2]/div/div/main/'

                                

                            except:
                                #sin boton
                                while(True):

                                    try:
                                        course = driver.find_element_by_xpath(x_path_actual+'/div[3]/ul/li['+str(int_course)+']/div/div[2]/div/div[1]/div/span/span[1]').text
                                        courses.append(course)
                                        int_course+=1
                                        

                                    except:
                                        break
                            
                            if(len(courses) == 0):
                                profile.append(float('NaN'))
                            else:
                                profile.append(courses)    
                            
                            driver.get(link_profile)
                            time.sleep(3)
                            
                            break

                        if(id=="experience"):

                            time.sleep(3)

                            experiences = []

                            try:
                            #con bot??n
                                see_more_experience_link = driver.find_element_by_xpath(x_path_actual+"/div[3]/div/a").get_attribute("href")
                                driver.get(see_more_experience_link)
                                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                                time.sleep(randint(3,5))

                                while(True):
                                    try:
                                        try:
                                            try:
                                                #sin link
                                                experience = []

                                                #titulo(cargo)
                                                experience.append(driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div/div[1]/div/span/span[2]').text)

                                                #1 ??? compa??ia y jornada, 2 ??? fecha, 3 ??? lugar
                                                for i in range(1,4):

                                                    if(i==1 or i==2):
                                                        aux = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div/div[1]/span['+str(i)+']/span[2]').text
                                                        aux_compania = aux.split('??')
                                                        experience.append(aux_compania[0])

                                                    else:
                                                        try:
                                                            experience.append(driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div/div[1]/span['+str(i)+']/span[2]').text)
                                                        except:
                                                            experience.append(float('NaN'))
                                                            pass

                                                experiences.append(experience)
                                                cont+=1

                                            except:
                                                
                                                #con link
                                                aux_empresa = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[1]/a/div/span/span[2]').text

                                                int_lista = 1
                                                cont_actual = cont

                                                while(True):

                                                    experience = []

                                                    try:
                                                        aux_cargo = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div/a/div/span/span[2]').text
                                                        aux_fecha_1 = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div/a/span/span[2]').text

                                                        if((any(map(str.isdigit, aux_fecha_1)))==True):

                                                            aux_fecha = aux_fecha_1.split('??')
                                                        
                                                            try:
                                                                aux_lugar = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[1]/a/span[2]/span[2]').text
                                                            except:
                                                                aux_lugar = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/span[2]/span[2]').text

                                                            

                                                        else:
                                                            aux_fecha_1 = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div/a/span[2]/span[1]').text
                                                            aux_fecha = aux_fecha_1.split('??')

                                                            try:
                                                                aux_lugar = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div/a/span[3]/span[1]').text
                                                            except:
                                                                aux_lugar = float('NaN')

                                                        experience.append(aux_cargo)
                                                        experience.append(aux_empresa)
                                                        experience.append(aux_fecha[0])
                                                        experience.append(aux_lugar)

                                                        experiences.append(experience)
                                                        
                                                        
                                                    except:
                                                        break

                                                    int_lista+=1
                                                cont+=1         

                                        except:

                                            try:
                                                experience = []
                                                #titulo(cargo)
                                                experience.append(driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div/div[1]/div/span/span[2]').text)

                                                #1 ??? compa??ia, 2 ??? fecha, 3 ??? lugar
                                                for i in range(1,4):

                                                    if(i==1 or i==2):
                                                        aux = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div/div[1]/span['+str(i)+']/span[2]').text
                                                        aux_compania = aux.split('??')
                                                        experience.append(aux_compania[0])

                                                    else:
                                                        try:
                                                            experience.append(driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div/div[1]/span['+str(i)+']/span[2]').text)
                                                        except:
                                                            experience.append(float('NaN'))

                                                experiences.append(experience)

                                                cont+=1

                                            except:
                                                #con link
                                                aux_empresa = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[1]/a/div/span/span[2]').text

                                                int_lista = 1
                                                cont_actual = cont

                                                while(True):

                                                    experience = []

                                                    try:
                                                        aux_cargo = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div/a/div/span/span[2]').text
                                                        aux_fecha_1 = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div/a/span/span[2]').text

                                                        if((any(map(str.isdigit, aux_fecha_1)))==True):

                                                            aux_fecha = aux_fecha_1.split('??')
                                                        
                                                            try:
                                                                aux_lugar = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[1]/a/span[2]/span[2]').text
                                                            except:
                                                                aux_lugar = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/span[2]/span[2]').text

                                                            

                                                        else:
                                                            aux_fecha_1 = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div/a/span[2]/span[1]').text
                                                            aux_fecha = aux_fecha_1.split('??')


                                                            try:
                                                                aux_lugar = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div/a/span[3]/span[1]').text
                                                            except:
                                                                aux_lugar = float('NaN')
                                                    

                                                        experience.append(aux_cargo)
                                                        experience.append(aux_empresa)
                                                        experience.append(aux_fecha[0])
                                                        experience.append(aux_lugar)

                                                        experiences.append(experience)
                                                        
                                                        
                                                    except:
                                                        break

                                                    int_lista+=1
                                                cont+=1

                                    except:
                                        break

                                

                            except:
                                #sin boton
                                while(True):

                                    try:

                                        try:
                                            try:
                                                #sin link
                                                experience = []
                                                experience.append(driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section['+str(int_section)+']/div[3]/ul/li['+str(cont)+']/div/div[2]/div[1]/div[1]/div/span/span[2]').text)
                                                for i in range(1,4):
                                                    if(i==1 or i==2):
                                                        aux = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section['+str(int_section)+']/div[3]/ul/li['+str(cont)+']/div/div[2]/div[1]/div[1]/span['+str(i)+']/span[2]').text
                                                        aux_compania = aux.split('??')
                                                        experience.append(aux_compania[0])

                                                    else:
                                                        try:
                                                            experience.append(driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section['+str(int_section)+']/div[3]/ul/li['+str(cont)+']/div/div[2]/div[1]/div[1]/span['+str(i)+']/span[2]').text)
                                                        except:
                                                            experience.append(float('NaN'))
                                                
                                                experiences.append(experience)
                                                cont+=1

                                            except:
                                                #con link
                                                aux_empresa = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section['+str(int_section)+']/div[3]/ul/li['+str(cont)+']/div/div[2]/div[1]/a/div/span/span[2]').text

                                                cont_actual = cont
                                                int_lista = 1

                                                experience = []
                                                

                                                while(True):

                                                    experience = []
                                                    try:
                                            
                                                        aux_cargo = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[3]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/div/span/span[2]').text
                                                        aux_fecha_1 = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[3]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/span[1]/span[1]').text
                                                        aux_fecha = aux_fecha_1.split('??')

                                                        try:
                                                            aux_lugar = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[3]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/span[2]/span[1]').text

                                                        except:
                                                            aux_lugar = float('NaN')

                                                        experience.append(aux_cargo)
                                                        experience.append(aux_empresa)
                                                        experience.append(aux_fecha[0])
                                                        experience.append(aux_lugar)

                                                        experiences.append(experience)
                                                    
                                                    except:
                                                        break

                                                    

                                                    int_lista+=1
                                                    
                                                cont +=1

                                        except:
                                            break

                                    except:

                                        try:
                                            try:
                                                #sin link
                                                experience = []
                                                experience.append(driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section['+str(int_section)+']/div[3]/ul/li['+str(cont)+']/div/div[2]/div[1]/div[1]/div/span/span[2]').text)
                                                for i in range(1,4):
                                                    if(i==1 or i==2):
                                                        aux = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section['+str(int_section)+']/div[3]/ul/li['+str(cont)+']/div/div[2]/div[1]/div[1]/span['+str(i)+']/span[2]').text
                                                        aux_compania = aux.split('??')
                                                        experience.append(aux_compania[0])

                                                    else:
                                                        try:
                                                            experience.append(driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section['+str(int_section)+']/div[3]/ul/li['+str(cont)+']/div/div[2]/div[1]/div[1]/span['+str(i)+']/span[2]').text)
                                                        except:
                                                            experience.append(float('NaN'))
                                                
                                                experiences.append(experience)
                                                cont+=1

                                            except:
                                                #con link
                                                aux_empresa = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section['+str(int_section)+']/div[3]/ul/li['+str(cont)+']/div/div[2]/div[1]/a/div/span/span[2]').text

                                                cont_actual = cont
                                                int_lista = 1

                                                experience = []
                                                
                                                while(True):

                                                    experience = []
                                                    try:
                                            
                                                        aux_cargo = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[3]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/div/span/span[2]').text
                                                        aux_fecha_1 = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[3]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/span[1]/span[1]').text
                                                        aux_fecha = aux_fecha_1.split('??')

                                                        try:
                                                            aux_lugar = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[3]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/span[2]/span[1]').text

                                                        except:
                                                            aux_lugar = float('NaN')

                                                        experience.append(aux_cargo)
                                                        experience.append(aux_empresa)
                                                        experience.append(aux_fecha[0])
                                                        experience.append(aux_lugar)

                                                        experiences.append(experience)
                                                    
                                                    except:
                                                        break

                                                    

                                                    int_lista+=1
                                                    
                                                cont +=1

                                        except:
                                            break
                            
                            if(len(experiences) == 0):
                                profile.append(float('NaN'))
                            else:
                                profile.append(experiences)

                            cont = 1
                            driver.get(link_profile)
                            time.sleep(3)
                            break
                            

                        if(id=="education"):

                            time.sleep(3)
                            
                            educacion = []
                            cont=1
                            #con boton
                            try:
                                see_more_education_link = driver.find_element_by_xpath(x_path_actual+"/div[3]/div/a").get_attribute("href")
                                driver.get(see_more_education_link)
                                time.sleep(3)

                                while(True):
                                    educacion_nombre = []
                                    try:          
                                        try:               
                                            educacion_nombre.append(driver.find_element_by_xpath(f"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/div/span/span[1]").text)
                                        except:
                                            try:
                                                educacion_nombre.append(driver.find_element_by_xpath(f"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/div/span/span[1]").text)
                                                
                                            except:
                                                break
                                        cont+=1
                                        educacion.append(educacion_nombre)
                                    except:
                                        break  
                                time.sleep(2)
                                #Texto
                                cont2=0
                                cont=1
                                while True:
                                    try:
                                        try:
                                            educacion[cont2].append(driver.find_element_by_xpath(f"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/span[1]/span[1]").text)    
                                        except:
                                            educacion[cont2].append(driver.find_element_by_xpath(f"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/span[1]/span[1]").text) 
                                        cont+=1
                                        cont2+=1
                                    except:
                                        break
                            #sin boton
                            except:
                                time.sleep(2)
                                #Titulo
                                while(True):
                                    educacion_nombre = []
                                    try:
                                        try:                                   
                                            educacion_nombre.append(driver.find_element_by_xpath(x_path_actual+"/div[3]/ul/li["+str(cont)+"]/div/div[2]/div/a/div/span/span[1]").text)
                                        except:
                                            educacion_nombre.append(driver.find_element_by_xpath(x_path_actual+"/div[3]/ul/li["+str(cont)+"]/div/div[2]/div/a/div/span/span[1]").text)
                                        cont+=1
                                        educacion.append(educacion_nombre)
                                    except:
                                        break
                                time.sleep(2)        
                                #texto
                                cont2=0
                                cont=1
                                while True:
                                    try:
                                        try:
                                            educacion[cont2].append(driver.find_element_by_xpath(x_path_actual+"/div[3]/ul/li["+str(cont)+"]/div/div[2]/div/a/span[1]/span[1]").text) 
                                        except:
                                            try:
                                                educacion[cont2].append(driver.find_element_by_xpath(x_path_actual+"/div[3]/ul/li["+str(cont)+"]/div/div[2]/div/a/span[1]/span[1]").text)
                                            except:
                                                break
                                        cont+=1
                                        cont2+=1
                                    except:
                                        break

                            if(educacion==[]):
                                profile.append(float('NaN'))
                            else:
                                profile.append(educacion)
                            
                            driver.get(link_profile)
                            time.sleep(2)
                            break


                        if(id=="licenses_and_certifications"):
                            
                            time.sleep(2)
                            
                            licencias = []
                            cont=1
                            try:
                                see_more_licenses_link = driver.find_element_by_xpath(x_path_actual+"/div[3]/div/a").get_attribute("href")
                                driver.get(see_more_licenses_link)
                                time.sleep(3)

                                #Nombre 
                                while(True):
                                    licencia_nombre  = [] 
                                    
                                    try:
                                        try:                            
                                            licencia_nombre.append(driver.find_element_by_xpath(f"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/div[1]/div/span/span[1]").text)
                                        except:
                                            try:
                                                licencia_nombre.append(driver.find_element_by_xpath(f"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/div[1]/div/span/span[1]").text)  
                                            except:
                                                try:
                                                    licencia_nombre.append(driver.find_element_by_xpath(f"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div/div[1]/div/span/span[1]").text)  
                                                except:
                                                    try:
                                                        licencia_nombre.append(driver.find_element_by_xpath(f"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div/div[1]/div/span/span[1]").text)  
                                                    except:
                                                        try:
                                                            licencia_nombre.append(driver.find_element_by_xpath(f"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/div/span/span[1]").text)
                                                        except:
                                                            licencia_nombre.append(driver.find_element_by_xpath(f"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/div/span/span[1]").text)  
                                        cont+=1
                                        licencias.append(licencia_nombre)

                                    except:
                                        break
                                
                                #Localidad 
                                time.sleep(2)
                                cont2=0
                                cont=1
                                while(True):  
                                    try:
                                        try:
                                            licencias[cont2].append(driver.find_element_by_xpath(f"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/span[1]/span[1]").text)          
                                        except:
                                            try:
                                                licencias[cont2].append(driver.find_element_by_xpath(f"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/span[1]/span[1]").text) 
                                            except:    
                                                try:
                                                    licencias[cont2].append(driver.find_element_by_xpath(f"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div/div[1]/span[1]/span[1]").text)    
                                                except:
                                                    try:
                                                        licencias[cont2].append(driver.find_element_by_xpath(f"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/div/span/span[1]").text)
                                                    except:
                                                        try:
                                                            licencias[cont2].append(driver.find_element_by_xpath(f"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/div/span/span[1]").text)
                                                        except:
                                                            licencias[cont2].append(driver.find_element_by_xpath(f"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div/div[1]/span[1]/span[1]").text)  
                                        cont+=1
                                        cont2+=1
                                        
                                    except:
                                        break
                                print(licencias)

                            #sin boton
                            except:
                                time.sleep(2)
                                #nombre
                                while(True):
                                    licencia_nombre  = [] 
                                    try:
                                        try: 
                                            licencia_nombre.append(driver.find_element_by_xpath(f"{x_path_actual}/div[3]/ul/li[{str(cont)}]/div/div[2]/div/div[1]/div/span/span[1]").text)
                                        except:
                                            try:
                                                licencia_nombre.append(driver.find_element_by_xpath(f"{x_path_actual}/div[3]/ul/li[{str(cont)}]/div/div[2]/div/div[1]/div/span/span[1]").text)
                                            except:
                                                licencia_nombre.append(driver.find_element_by_xpath(f"{x_path_actual}/div[3]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/div/span/span[1]").text)
                                        cont+=1
                                        licencias.append(licencia_nombre)
                                    except:
                                        break
                                time.sleep(2)
                                #Lugar
                                cont2=0
                                cont=1
                                while(True):  
                                    try:
                                        try:
                                            licencias[cont2].append(driver.find_element_by_xpath(f"{x_path_actual}/div[3]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/span[1]/span[1]").text)          
                                        except:
                                            try:
                                                licencias[cont2].append(driver.find_element_by_xpath(f"{x_path_actual}/div[3]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/span[1]/span[1]").text)
                                            except:
                                                licencias[cont2].append(driver.find_element_by_xpath(f"{x_path_actual}/div[3]/ul/li[{str(cont)}]/div/div[2]/div/div[1]/span/span[1]").text)

                                        cont+=1
                                        cont2+=1
                                    except:
                                        break
                            
                            if(licencias==[]):
                                profile.append(float('NaN'))
                            else:
                                profile.append(licencias)

                            driver.get(link_profile)
                            time.sleep(3)
                            break

                        if(id=="skills"):
                            
                            all_skills = []

                            try:
                                see_more_skills_link = driver.find_element_by_xpath(x_path_actual+"/div[3]/div/a").get_attribute("href")
                                driver.get(see_more_skills_link)
                                time.sleep(3)

                                while(True):
                                    try:
                                        try:                            
                                            skill = driver.find_element_by_xpath(f"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/div/span[1]/span[1]").text
                                        except:
                                            try:
                                                skill = driver.find_element_by_xpath(f"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/a/div/span[1]/span[1]").text
                                            except:
                                                try:
                                                    skill = driver.find_element_by_xpath(f"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/div[1]/div/span/span[1]").text
                                                except:
                                                    skill = driver.find_element_by_xpath(f"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div[1]/div[1]/div/span/span[1]").text
                                        cont+=1
                                        all_skills.append(skill)
                                    except:
                                        break
                            except:
                                while(True):
                                    try:
                                        try:                                        #/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li[11]/div/div[2]/div[1]/div[1]/div/span/span[1]  
                                            skill = driver.find_element_by_xpath(f"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section[4]/div[3]/ul/li[{str(cont)}]/div/div[2]/div[1]/div[1]/div/span/span[1]").text
                                        except:
                                            skill = driver.find_element_by_xpath(f"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[4]/div[3]/ul/li[{str(cont)}]/div/div[2]/div[1]/div[1]/div/span/span[1]").text
                                        cont+=1
                                        all_skills.append(skill)

                                    except:
                                        break
                                        
                            if(all_skills==[]):
                                profile.append(float('NaN'))
                            else:
                                profile.append(all_skills)

                            driver.get(link_profile)
                            time.sleep(3)
                                
                            break

                        if(id=="languages"):
                            
                            time.sleep(3)
                            cont=1
                            
                            idiomas = []

                            try:
                                see_more_languages_link = driver.find_element_by_xpath(x_path_actual+"/div[3]/div/a").get_attribute("href")
                                driver.get(see_more_languages_link)
                                time.sleep(3)

                                while(True):
                                    try:
                                        try:                            
                                            idioma_nombre = driver.find_element_by_xpath(f"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div/div[1]/div/span/span[1]").text
                                        except:
                                            idioma_nombre = driver.find_element_by_xpath(f"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{str(cont)}]/div/div[2]/div/div[1]/div/span/span[1]").text
                                        cont+=1
                                        idiomas.append(idioma_nombre)
                                    except:
                                        break
                            #sin boton
                            except:
                                time.sleep(2)
                                while(True):
                                    try:
                                        idioma_nombre = driver.find_element_by_xpath(x_path_actual+"/div[3]/ul/li["+str(cont)+"]/div/div[2]/div/div[1]/div/span/span[1]").text
                                        idiomas.append(idioma_nombre)
                                        cont+=1
                                                                                    
                                    except:
                                        break

                            if(idiomas==[]):
                                profile.append(float('NaN'))
                            else:
                                profile.append(idiomas)

                            driver.get(link_profile)
                            time.sleep(2)
                            cont=1
                            break

                        if(id=="recommendations"):
                            
                            recomendaciones = []

                            try:
                                #con boton
                                see_more_recommendations_link = driver.find_element_by_xpath(x_path_actual+'/div[3]/div[2]/div/div/a').get_attribute('href')
                                driver.get(see_more_recommendations_link)
                                int_lista_recomendaciones = 1

                                time.sleep(randint(3,5))

                                try:

                                    driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[1]/a/div/span[1]/span[2]').text

                                    while(True):

                                        try:

                                            recomendacion = []

                                            recomendador = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[1]/a/div/span[1]/span[2]').text
                                            cargo = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[1]/a/span[1]/span[2]').text
                                            recomendacion_texto = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[2]/ul/li/div/ul/li/div/div/div/span[2]').text
                                            
                                            recomendacion.append(recomendador)
                                            recomendacion.append(cargo)
                                            recomendacion.append(recomendacion_texto)

                                            recomendaciones.append(recomendacion)

                                            int_lista_recomendaciones+=1


                                        except:

                                            break

                                except:

                                    driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[1]/a/div/span[1]/span[2]').text

                                    while(True):

                                        try:

                                            recomendacion = []

                                            recomendador = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[1]/a/div/span[1]/span[2]').text
                                            cargo = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[1]/a/span[1]/span[2]').text
                                            recomendacion_texto = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[2]/ul/li/div/ul/li/div/div/div/span[2]').text
                                            
                                            recomendacion.append(recomendador)
                                            recomendacion.append(cargo)
                                            recomendacion.append(recomendacion_texto)

                                            recomendaciones.append(recomendacion)

                                            int_lista_recomendaciones+=1

                                        except:

                                            break

                            except:
                                #sin boton

                                int_lista_recomendaciones = 1

                                try:
                                    driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[3]/div[2]/div/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[1]/a/div/span[1]/span[2]').text

                                    while(True):
                                        
                                        try:

                                            recomendacion = []

                                            recomendador = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[3]/div[2]/div/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[1]/a/div/span[1]/span[2]').text
                                            cargo = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[3]/div[2]/div/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[1]/a/span[1]/span[2]').text
                                            recomendacion_texto = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[3]/div[2]/div/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[2]/ul/li/div/ul/li/div/div/div/div/span[1]').text
                                                                            

                                            recomendacion.append(recomendador)
                                            recomendacion.append(cargo)
                                            recomendacion.append(recomendacion_texto)

                                            recomendaciones.append(recomendacion)
                                            
                                            

                                        except:
                                            break

                                        int_lista_recomendaciones+=1

                                    

                                except:

                                    driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[3]/div[2]/div/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[1]/a/div/span[1]/span[2]').text

                                    while(True):

                                        try:

                                            recomendacion = []

                                            recomendador = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[3]/div[2]/div/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[1]/a/div/span[1]/span[2]').text
                                            cargo = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[3]/div[2]/div/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[1]/a/span[1]/span[2]').text
                                            recomendacion_texto = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[3]/div[2]/div/ul/li['+str(int_lista_recomendaciones)+']/div/div[2]/div[2]/ul/li/div/ul/li/div/div/div/div/span[1]').text

                                            recomendacion.append(recomendador)
                                            recomendacion.append(cargo)
                                            recomendacion.append(recomendacion_texto)

                                            recomendaciones.append(recomendacion)


                                        except:
                                            break

                                        int_lista_recomendaciones+=1    

                            if(recomendaciones == []):
                                profile.append(float('NaN'))
                            else:
                                profile.append(recomendaciones)
                            break

                    except:
                        int_section+=1
                        

                    if(int_section>20):
                        #si no encuentra una seccion, quiere decir que no tiene esa info y se guarda un array vacio
                        profile.append(float('NaN'))
                        break

            print(profile)

            if condicion == True:
                datas=pd.DataFrame(data_key)
                datas.to_csv('dataset_practica.csv',sep=",",encoding="utf-8",mode="a",index=False)
                condicion = False

            try:
                data ={
                    'Details': [profile[0]],
                    'About': [profile[1]],
                    'Courses': [profile[2]],
                    'Experience': [profile[3]],
                    'Education': [profile[4]],
                    'Licenses and certifications': [profile[5]],
                    'Skills': [profile[6]],
                    'Languages': [profile[7]],
                    'Recommendations': [profile[8]]
                }

                datas=pd.DataFrame(data)
                datas.to_csv('dataset_practica.csv',encoding='utf-8',sep=',',mode="a",header=False,index=False)
            except:
                pass

            cont_profiles +=1

        except:
            pass

        

    driver.close()
    int_txt+=1
    time.sleep(3)  

new_df = pd.read_csv('dataset_practica.csv')
print(new_df)