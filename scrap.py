from selenium import webdriver
import time
from random import randint

driver = webdriver.Chrome()
driver.maximize_window()

int_txt = 1
caracter_comillas = "'"

mail_password =[['distintosuso@gmail.com','uno23456789']]
array_ids = ["about", "courses", "honors_and_awards", "experience", "education", "licenses_and_certifications", "skills", "languages", "recommendations", "final"]

all_profiles = []

for i in mail_password:

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

        time.sleep(10)

        data_basic = []
        int_div_main = 5

        name = ''
        work = ''
        location = ''

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

            if(id=="final"):
                break

            #para corroborar que el div cambia al volver al perfil, sino lo cambia por otro número

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
                        
                        about_profile = driver.find_element_by_xpath(x_path_actual+"/div[3]/div/div/div/span[1]").text
                        profile.append(about_profile)
                        break

                    if(id=="courses"):

                        courses = []
                        int_course = 1

                        try:
                            #con boton
                            see_more_courses_link = driver.find_element_by_xpath(x_path_actual+'/div[3]/div/a').get_attribute('href')
                            driver.get(see_more_courses_link)
                            time.sleep(15)

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

                            driver.get(link_profile)

                        except:
                            #sin boton
                            while(True):

                                try:
                                    course = driver.find_element_by_xpath(x_path_actual+'/div[3]/ul/li['+str(int_course)+']/div/div[2]/div/div[1]/div/span/span[1]').text
                                    courses.append(course)
                                    int_course+=1
                                    

                                except:
                                    break
                            
                        profile.append(courses)
                        
                        break

                    if(id=="honors_and_awards"):
                       profile.append("TIENE RECONOCIMIENTOS Y PREMIOS")
                       break

                    if(id=="experience"):

                        experiences = []

                        try:
                        #con botón
                            see_more_experience_link = driver.find_element_by_xpath(x_path_actual+"/div[3]/div/a").get_attribute("href")
                            driver.get(see_more_experience_link)
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                            time.sleep(randint(5,7))

                            while(True):
                                try:
                                    try:
                                        try:
                                            #sin link
                                            experience = []

                                            #titulo(cargo)
                                            experience.append(driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div/div[1]/div/span/span[2]').text)

                                            #1 → compañia y jornada, 2 → fecha, 3 → lugar
                                            for i in range(1,4):

                                                if(i==1 or i==2):
                                                    aux = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div/div[1]/span['+str(i)+']/span[2]').text
                                                    aux_compania = aux.split('·')
                                                    experience.append(aux_compania[0])

                                                else:
                                                    try:
                                                        experience.append(driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div/div[1]/span['+str(i)+']/span[2]').text)
                                                    except:
                                                        experience.append('0')
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

                                                        aux_fecha = aux_fecha_1.split('·')
                                                    
                                                        try:
                                                            aux_lugar = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[1]/a/span[2]/span[2]').text
                                                        except:
                                                            aux_lugar = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/span[2]/span[2]').text

                                                        

                                                    else:
                                                        aux_fecha_1 = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div/a/span[2]/span[1]').text
                                                        aux_fecha = aux_fecha_1.split('·')

                                                        try:
                                                            aux_lugar = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div/a/span[3]/span[1]').text
                                                        except:
                                                            aux_lugar = '0'

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

                                            #1 → compañia, 2 → fecha, 3 → lugar
                                            for i in range(1,4):

                                                if(i==1 or i==2):
                                                    aux = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div/div[1]/span['+str(i)+']/span[2]').text
                                                    aux_compania = aux.split('·')
                                                    experience.append(aux_compania[0])

                                                else:
                                                    try:
                                                        experience.append(driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div/div[1]/span['+str(i)+']/span[2]').text)
                                                    except:
                                                        experience.append('0')

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

                                                        aux_fecha = aux_fecha_1.split('·')
                                                    
                                                        try:
                                                            aux_lugar = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[1]/a/span[2]/span[2]').text
                                                        except:
                                                            aux_lugar = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/span[2]/span[2]').text

                                                        

                                                    else:
                                                        aux_fecha_1 = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div/a/span[2]/span[1]').text
                                                        aux_fecha = aux_fecha_1.split('·')


                                                        try:
                                                            aux_lugar = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li['+str(cont)+']/div/div[2]/div[2]/ul/li/div/div/div[1]/ul/li['+str(int_lista)+']/div/div[2]/div/a/span[3]/span[1]').text
                                                        except:
                                                            aux_lugar = '0'
                                                

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
                                                    aux_compania = aux.split('·')
                                                    experience.append(aux_compania[0])

                                                else:
                                                    try:
                                                        experience.append(driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section['+str(int_section)+']/div[3]/ul/li['+str(cont)+']/div/div[2]/div[1]/div[1]/span['+str(i)+']/span[2]').text)
                                                    except:
                                                        experience.append('0')
                                            
                                            experiences.append(experience)
                                            cont+=1

                                        except:
                                            #con link
                                            aux_empresa = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section['+str(int_section)+']/div[3]/ul/li['+str(cont)+']/div/div[2]/div[1]/a/div/span/span[2]').text

                                            cont_actual = cont
                                            int_lista = 1

                                            experience = []
                                            
                                            print(aux_empresa)
                                            

                                            while(True):

                                                experience = []
                                                try:
                                        
                                                    aux_cargo = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[3]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/div/span/span[2]').text
                                                    aux_fecha_1 = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[3]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/span[1]/span[1]').text
                                                    aux_fecha = aux_fecha_1.split('·')

                                                    try:
                                                        aux_lugar = driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/section/div[3]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/span[2]/span[1]').text

                                                    except:
                                                        aux_lugar = '0'

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
                                                    aux_compania = aux.split('·')
                                                    experience.append(aux_compania[0])

                                                else:
                                                    try:
                                                        experience.append(driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section['+str(int_section)+']/div[3]/ul/li['+str(cont)+']/div/div[2]/div[1]/div[1]/span['+str(i)+']/span[2]').text)
                                                    except:
                                                        experience.append('0')
                                            
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
                                                    aux_fecha = aux_fecha_1.split('·')

                                                    try:
                                                        aux_lugar = driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[3]/ul/li['+str(cont_actual)+']/div/div[2]/div[2]/ul/li['+str(int_lista)+']/div/div[2]/div[1]/a/span[2]/span[1]').text

                                                    except:
                                                        aux_lugar = '0'

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

                        profile.append(experiences)
                        cont = 1
                        driver.get(link_profile)
                        break

                    if(id=="education"):
                        profile.append("TIENE EDUCACION")
                        break

                    if(id=="licenses_and_certifications"):
                        profile.append("TIENE LICENCIAS")
                        break

                    if(id=="skills"):
                        profile.append("TIENE APTITUDES")
                        break

                    if(id=="languages"):
                        profile.append("TIENE IDIOMAS")
                        break

                    if(id=="recommendations"):
                        recomendaciones = []

                        try:
                            #con boton
                            see_more_recommendations_link = driver.find_element_by_xpath(x_path_actual+'/div[3]/div[2]/div/div/a').get_attribute('href')
                            driver.get(see_more_recommendations_link)
                            int_lista_recomendaciones = 1

                            time.sleep(randint(5,7))

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

                        profile.append(recomendaciones)
                        break

                except:
                    int_section+=1
                    

                if(int_section>20):
                    #si no encuentra una seccion, quiere decir que no tiene esa info y se guarda un array vacio
                    profile.append([])
                    break

            
        print(profile)
        

    

    break

            





