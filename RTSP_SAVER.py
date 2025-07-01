
import os
import time
import tkinter
import cv2
import numpy
import random
import hashlib
from Cryptodome.Util.Padding import pad,unpad
import datetime
from Cryptodome.Cipher import AES
import gc
import sys
import multiprocessing
import queue
Version = "V1_01.07.2025"

global_root_t_string_start = "2024-01-31 14:00:00"
global_root_t_string_ende = "2027-04-20 14:00:00"

class dahua_stream_multithreaded():
    queobj = ""
    threadobj = ""
    captureobj = ""
    def __init__(self,USERNAME,PASSWORD,ADDRESS,CHANNELSELECT,STREAMSELECT,buffer_size_int):
        threadobjj = threading.Thread(target=get_frames, daemon=True)
        threadobjj.start()

    def get_frames(self):
        while True:
            try:
                self.queobj.put(self.captureobj.read()[1],timeout=1)
                #pipeobj.put(capture.read()[1], timeout=0)
            except Exception as X:
                pass
                #print(X)
                #print("que full" + str(time.asctime()))

    def gen_queue(self,buffer_size_int):
        self.queobj = queue.Queue(buffer_size)

    def start_video_cap(self,USERNAME,PASSWORD,ADDRESS,CHANNELSELECT,STREAMSELECT,):
        self.captureobj  = cv2.VideoCapture(str("rtsp://" + USERNAME + ":" + PASSWORD + "@" + ADDRESS + '/cam/realmonitor?channel=' + CHANNELSELECT + '&subtype=' + STREAMSELECT))

    def close_obj(self):
        del self.captureobj
        self.threadobj.close()
        self.captureobj.release()

def filtering_a_list_of_indixes_with_two_timedeltastrings(time_str1,time_str2,list_of_files):
    def extract_time_from_index_file_string(eingabe_string):
        if type(eingabe_string) != str:
            raise Exception("type is not str")

        neuer_str = eingabe_string.split(" ")[0:-2]
        neuer_str = str(neuer_str[-2] + " " + str(neuer_str[-1]))
        neuer_str = neuer_str[0:-7]
        #print(neuer_str)
        return neuer_str
    def generate_time_obj_out_of_string(eingabe_string):
        if type(eingabe_string) != str:
            raise Exception("type is not str")
        print("eingabestr von zeile 27: " + eingabe_string)

        trenzeichen_1 = str(eingabe_string[4])
        trenzeichen_2 = str(eingabe_string[-3])

        datetime_object = datetime.datetime.strptime(eingabe_string, ("%Y" + trenzeichen_1 + "%m" + trenzeichen_1 + "%d" + " " + "%H" + trenzeichen_2 + "%M" + trenzeichen_2 + "%S"))
        #print(datetime_object)
        return datetime_object

    if type(time_str1) and type(time_str2) != str:
        raise Exception("time is not str")
    if type(list_of_files) != list:
        raise Exception("is not type list")
    list_of_files.sort()
    #string 1 und 2 sollen so ausehen 2023-01-31 14:16:01
    time_obj_start = generate_time_obj_out_of_string(time_str1)
    time_obj_end = generate_time_obj_out_of_string(time_str2)
    #print(str(time_obj_start) + " " + str(time_obj_end))
    liste_richtiger_files = []
    liste_timeobj_zu_eingabe_liste = []

    for i in list_of_files:
        print(i)
        time_for_loop_1 = extract_time_from_index_file_string(i)
        liste_timeobj_zu_eingabe_liste.append(generate_time_obj_out_of_string(time_for_loop_1))
    for i in list_of_files:
        #print(liste_timeobj_zu_eingabe_liste[0])

        if liste_timeobj_zu_eingabe_liste[0] >= time_obj_start and liste_timeobj_zu_eingabe_liste[0] <= time_obj_end:
            liste_richtiger_files.append(list_of_files[0])
            #print(i + " zeile 60" + str(time_obj_start) + " " + str(time_obj_end))
            #print(liste_timeobj_zu_eingabe_liste[0])
        del list_of_files[0]
        del liste_timeobj_zu_eingabe_liste[0]

    return liste_richtiger_files
def opencamerastream(ADDRESS, USERNAME, PASSWORD, CHANNELSELECT, STREAMSELECT, speicher_resolution, anzahl_frame_batch,pw_string, pipe,max_speicher,live_resoltion_1,live_resoltion_2,encryption_option):
    def get_size_delete_overfill(start_path, dir_limit_in_gb):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        total_size_kb = total_size / 1000
        total_size_mb = total_size_kb / 1000
        total_size_gb = total_size_mb / 1000

        while dir_limit_in_gb < total_size_gb:
            list_of_old_entries = os.listdir(start_path)
            os.remove(start_path + list_of_old_entries[0])
            os.remove(start_path + list_of_old_entries[1])
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(start_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    # skip if it is symbolic link
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
            total_size_kb = total_size / 1000
            total_size_mb = total_size_kb / 1000
            total_size_gb = total_size_mb / 1000

    while True:
        try:
            """
            capture = cv2.VideoCapture(
                str("rtsp://" + USERNAME + ":" + PASSWORD + "@" + ADDRESS + '/cam/realmonitor?channel=' + CHANNELSELECT + '&subtype=' + STREAMSELECT))
            #print(str("rtsp://" + USERNAME + ":" + PASSWORD + "@" + ADDRESS + '/cam/realmonitor?channel=' + CHANNELSELECT + '&subtype=' + STREAMSELECT))
            """
            captureobj = dahua_stream_multithreaded(USERNAME, PASSWORD, ADDRESS, CHANNELSELECT, STREAMSELECT, 5)

            frame_number = 0

            test = str(os.path.abspath(os.getcwd()))
            print(test)
            string_path = test + "/records/" + str(ADDRESS) + "/"
            frame_buffer_list = bytearray()
            grund_dir = "./records/"

            if sys.platform == "linux":
                pass
                # print(sys.platform)
            else:
                string_path = string_path.replace("\\", r"/")
                grund_dir = grund_dir.replace("\\", "/")

            try:
                os.mkdir(grund_dir)
            except Exception as x:
                print(x)

            try:
                os.mkdir(string_path)
            except Exception as x:
                print(x)
            first_frame = captureobj.queobj.get()
            while True:
                if encryption_option != "encryption_on":
                    while True:
                        if speicher_resolution[0] == 0 or speicher_resolution[1] == 0:
                            while True:
                                frame = captureobj.queobj.get()
                                frame_live = cv2.resize(frame, (int(live_resoltion_1), int(live_resoltion_2)))
                                cv2.imshow(str(ADDRESS), frame_live)
                                cv2.waitKey(1)
                                first_frame = frame
                        if frame_number == 0:
                            get_size_delete_overfill(string_path, max_speicher)
                            rand = random.SystemRandom()
                            rand_hex = "x" + str(hex(int(rand.getrandbits(20)))) + "x"
                            string_for_file_name = string_path + str(ADDRESS) + "  " + str(datetime.datetime.now()).replace(":", "_") + " " + rand_hex + ".mp4"

                            fourcc = cv2.VideoWriter_fourcc(*'mp4v')

                            out = cv2.VideoWriter(string_for_file_name, fourcc, 25, speicher_resolution) # replace with ipcam Framerrate


                        frame = captureobj.queobj.get()
                        frame = cv2.resize(frame, speicher_resolution,interpolation=cv2.INTER_LINEAR)  # fastest oneporn
                        out.write(frame)

                        if int(live_resoltion_1) != 0 or int(live_resoltion_2) != 0:
                            # frame_live = cv2.resize(frame, (int(live_resoltion_1),int(live_resoltion_2)))
                            frame_live = cv2.resize(frame, (int(live_resoltion_1), int(live_resoltion_2)),
                                                    interpolation=cv2.INTER_LINEAR)  # fastest one
                            cv2.imshow(str(ADDRESS), frame_live)
                            cv2.waitKey(1)

                        frame_number = frame_number + 1

                        if frame_number == anzahl_frame_batch:
                            out.release()
                            frame_number = 0

                if speicher_resolution[0] == 0 or speicher_resolution[1] == 0:
                    while True:
                        frame = captureobj.queobj.get()
                        frame_live = cv2.resize(frame, (int(live_resoltion_1), int(live_resoltion_2)))
                        cv2.imshow(str(ADDRESS), frame_live)
                        cv2.waitKey(1)


                if frame_number == 0:
                    frame = captureobj.queobj.get()
                    get_size_delete_overfill(string_path, max_speicher)
                    rand = random.SystemRandom()
                    rand_hex = "x" + str(hex(int(rand.getrandbits(20)))) + "x"
                    string_for_encrypted_file_name = string_path + str(ADDRESS) + "  " + str(
                        datetime.datetime.now()).replace(":", "_") + " "+ rand_hex
                    string_for_encrypted_file_name_index = string_for_encrypted_file_name + " indexform"
                    # writeobj_for_encrypted_jpg = open(string_for_encrypted_file_name, "wb")
                    # nach unten zum batch ende verlagert

                    rand_int = int(rand.getrandbits(80))
                    salt = str(rand_int)
                    pw_string = pw_string + salt

                    aes_obj = rtsp_saver()
                    aes_obj.pkdf_2(pw_string)

                frame = captureobj.queobj.get()

                #print(numpy.shape(frame))
                #print(numpy.shape(frame_live))

                #print(speicher_resolution)
                #frame = cv2.resize(frame, speicher_resolution)
                frame = cv2.resize(frame, speicher_resolution, interpolation=cv2.INTER_LINEAR) #fastest one
                if int(live_resoltion_1) != 0 or int(live_resoltion_2) != 0:
                    #frame_live = cv2.resize(frame, (int(live_resoltion_1),int(live_resoltion_2)))
                    frame_live = cv2.resize(frame, (int(live_resoltion_1),int(live_resoltion_2)),interpolation=cv2.INTER_LINEAR) #fastest one
                    cv2.imshow(str(ADDRESS),frame_live)
                    cv2.waitKey(1)
                frame = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])[1]
                aes_obj.encrypt_jpg(bytearray(frame))

                # writeobj_for_encrypted_jpg.write(aes_obj.array_encrypted_jpg_list[0])
                # del aes_obj.array_encrypted_jpg_list[:]
                frame_number += 1

                if frame_number == anzahl_frame_batch:

                    writeobj_for_encrypted_jpg = open(string_for_encrypted_file_name, "wb")
                    for i in aes_obj.array_encrypted_jpg_list:
                        writeobj_for_encrypted_jpg.write(i)
                    writeobj_for_encrypted_jpg.close()
                    indexfile = open(string_for_encrypted_file_name_index, "w")

                    # print(int.from_bytes(aes_obj.IV,"big"))
                    indexfile.write(str(int.from_bytes(aes_obj.IV, "big")) + "\n")
                    indexfile.write(
                        str(aes_obj.pw_abgleich_mit_index_fur_export) + "\n")  # zum veryfizieren nacher beim mp4 export damit ein pw wechsel des nutzers möglich ist bzw erkannt wird
                    indexfile.write(str(speicher_resolution) + "\n")
                    indexfile.write(salt + "\n")
                    for i in aes_obj.list_index_info:
                        indexfile.write(i)

                    indexfile.close()

                    frame_number = 0

            capture.release()
        except Exception as x:
            try:
                fileobj = open("Error","a")
                time_str = str(datetime.datetime.now())
                fileobj.write(time_str + ": " + str(x) + str(x.__class__) + "\n")
                fileobj.close()
            except:
                pass
            time.sleep(60)
prozesliste = []
que_liste = []
root = tkinter.Tk()
root.title("Dahua RTSP Saver")
def t_check():
    #global_root_t_string_start = "2023-01-31 14:00:00"
    global_root_t_string_ende = "2027-04-20 14:00:00"
    trenzeichen_1 = "-"
    trenzeichen_2 = ":"
    global_root_t_string_start_obj = datetime.datetime.strptime(global_root_t_string_start, ("%Y" + trenzeichen_1 + "%m" + trenzeichen_1 + "%d" + " " + "%H" + trenzeichen_2 + "%M" + trenzeichen_2 + "%S"))
    global_root_t_string_ende_obj  = datetime.datetime.strptime(global_root_t_string_ende, ("%Y" + trenzeichen_1 + "%m" + trenzeichen_1 + "%d" + " " + "%H" + trenzeichen_2 + "%M" + trenzeichen_2 + "%S"))

    new_var = datetime.datetime.now()
    if global_root_t_string_start_obj <= new_var and global_root_t_string_ende_obj >= new_var:
        return True
    else:
        return False

class rtsp_saver():
    # import hashlib
    def __init__(self):
        self.pw = ""
        self.aes_obj = ""
        self.array_encrypted_jpg_list = []
        self.list_index_info = []
        self.IV = ""
        self.pw_abgleich_mit_index_fur_export = ""

    def pkdf_2(self,pw_string):
        if type(pw_string) != str:
            return Exception("pw_string type is not type str")


        bytearray_of_pw = bytearray(pw_string,"UTF-8")
        pw_deriv_counter = 0
        hashobj = hashlib.sha3_256()

        while pw_deriv_counter != 300000:
            pw_deriv_counter = pw_deriv_counter + 1
            hashobj.update(bytearray_of_pw)
            bytearray_of_pw = hashobj.digest()

            """print(rundencounter," ",pw_deriv_counter)"""
        pw_array = hashobj.digest()

        self.aes_obj = AES.new(pw_array,AES.MODE_CBC)
        self.IV = self.aes_obj.IV
        #print(self.IV)

        bytearray_of_pw = pw_array
        pw_deriv_counter = 0
        hashobj = hashlib.sha3_256()

        while pw_deriv_counter != 300000:
            pw_deriv_counter = pw_deriv_counter + 1
            hashobj.update(bytearray_of_pw)
            bytearray_of_pw = hashobj.digest()

            """print(rundencounter," ",pw_deriv_counter)"""
        self.pw_abgleich_mit_index_fur_export = hashobj.digest()


        return pw_array

    def pkdf_2_decryption(self,pw_string,IV):
        if type(pw_string) != str:
            return Exception("pw_string type is not type str")


        bytearray_of_pw = bytearray(pw_string,"UTF-8")
        pw_deriv_counter = 0
        hashobj = hashlib.sha3_256()

        while pw_deriv_counter != 300000:
            pw_deriv_counter = pw_deriv_counter + 1
            hashobj.update(bytearray_of_pw)
            bytearray_of_pw = hashobj.digest()

            """print(rundencounter," ",pw_deriv_counter)"""
        pw_array = hashobj.digest()

        self.aes_obj = AES.new(pw_array,AES.MODE_CBC,iv=IV)

        bytearray_of_pw = pw_array
        pw_deriv_counter = 0
        hashobj = hashlib.sha3_256()

        while pw_deriv_counter != 300000:
            pw_deriv_counter = pw_deriv_counter + 1
            hashobj.update(bytearray_of_pw)
            bytearray_of_pw = hashobj.digest()

            """print(rundencounter," ",pw_deriv_counter)"""
        self.pw_abgleich_mit_index_fur_export = hashobj.digest()


        return pw_array




    def encrypt_jpg(self,jpg_array):
        randobj = random.SystemRandom()
        sidechannel_int_1 = int(randobj.getrandbits(10)) + 1
        sidechannel_int_2 = int(randobj.getrandbits(10)) + 1
        sidechannel_int_3 = int(randobj.getrandbits(10)) + 1
        pow(sidechannel_int_1,sidechannel_int_2,sidechannel_int_3)
        array = self.aes_obj.encrypt(pad(jpg_array,AES.block_size))
        self.array_encrypted_jpg_list.append(array)
        self.list_index_info.append(str(str(len(array)) + "," + str(datetime.datetime.now()) + "\n"))

    def decrypt_jpg(self, jpg_array):
        jpg_array = unpad(self.aes_obj.decrypt(jpg_array, ), AES.block_size)
        fileobj = open("beispiel.jpg", "wb")
        fileobj.write(jpg_array)
        return jpg_array
class conf_datei():

    def conf_datei_pkdf_2(self, pw_string):
        if type(pw_string) != str:
            return Exception("pw_string type is not type str")

        bytearray_of_pw = bytearray(pw_string, "UTF-8")
        pw_deriv_counter = 0
        hashobj = hashlib.sha3_256()

        while pw_deriv_counter != 300000:
            pw_deriv_counter = pw_deriv_counter + 1
            hashobj.update(bytearray_of_pw)
            bytearray_of_pw = hashobj.digest()

            """print(rundencounter," ",pw_deriv_counter)"""
        pw_array = hashobj.digest()
        return pw_array

    def check_for_conf(self):
        try:
            fileobj = open("conf","r")
            fileobj.read()
            fileobj.close()
            return True
        except:
            return False


    def create_overwririte_existingconf(self,pw_string,list_ip_number_strings_with_data_limit):
        if type(pw_string) != str:
            raise Exception("Type error is not string")
        if type(list_ip_number_strings_with_data_limit) != list:
            raise Exception("type error. is not list")
        for i in list_ip_number_strings_with_data_limit:
            if type(i) != str:
                raise Exception("list is not allowed to contain non string elements")


        if self.check_for_conf() == True:
            try:
                os.remove("conf")
            except:
                pass
        fileobj = open("conf","w")
        rand = random.SystemRandom()
        rand_int = int(rand.getrandbits(80))
        salt = str(rand_int)
        #sha enshres 256 bit len
        hashed_pw_salt = self.conf_datei_pkdf_2((pw_string + salt))
        test_str = "Test"
        fileobj.writelines((salt + "\n"))
        aesobj = AES.new(hashed_pw_salt,AES.MODE_ECB)
        test_array_for_veryfication = aesobj.encrypt(pad(bytearray(test_str,"UTF-8"),AES.block_size))
        veryfication_int = str(int.from_bytes(test_array_for_veryfication,"big"))
        #print(veryfication_int)
        fileobj.writelines((veryfication_int + "\n"))
        hinweis_str = "Format the adresses like this: 192.168.1.1,60,2000,2000,camerauser,password,live_res_1_number,live_res_2_number\n"
        hinweis_str2 = "Adress,max gigabyte to save for this camera,save with x pixel height,save with x pixel wide,user of the ipc,password ipc user,live show height,live show wide\n"
        hinweis_str3 = "Do not Change this line and above!\n"
        fileobj.writelines(hinweis_str)
        fileobj.writelines(hinweis_str2)
        fileobj.writelines(hinweis_str3)

        for i in list_ip_number_strings_with_data_limit:
            fileobj.writelines(i + "\n")
        fileobj.close()

    def check_if_pw_is_correct(self,pw_string):
        if type(pw_string) != str:
            raise Exception("type error. pw is not str")

        if self.check_for_conf() == False:
            return False
        fileobj = open("conf","r")
        salt = fileobj.readline()
        test_str = "Test"

        array_for_hash = self.conf_datei_pkdf_2(pw_string + str(int(salt)))
        aesobj = AES.new(array_for_hash, AES.MODE_ECB)
        test_array_for_veryfication = aesobj.encrypt(pad(bytearray(test_str, "UTF-8"), AES.block_size))
        veryfication_int = str(int.from_bytes(test_array_for_veryfication, "big"))
        #print(veryfication_int)
        check_int = int(fileobj.readline())
        #print(check_int)
        fileobj.close()
        if str(veryfication_int) == str(check_int):
            return True
        else:
            return False

    def get_cam_info_from_config(self):

        fileobj = open("conf","r")
        fileobj.readline()
        fileobj.readline()
        fileobj.readline()
        fileobj.readline()
        fileobj.readline()

        reststring = fileobj.read()
        fileobj.close()
        if reststring[-1] == "\n":
            reststring = reststring[:-1]
        if reststring[-1] == "\n":
            reststring = reststring[:-1]
        reststring = reststring.replace("\n",",")
        #print(reststring)


        infoliste = reststring.split(",")
        liste_info_einzeln = []
        #print(infoliste)
        for i in infoliste:
            if i != ",":
                liste_info_einzeln.append(i)
        #print(liste_info_einzeln)
        return liste_info_einzeln


    def get_conf_text(self):
        if self.check_for_conf() == True:
            fileobj = open("conf","r")
            string_conf = fileobj.read()
            fileobj.close()
            return string_conf
    def save_new_conf_text(self,conf_string):
        if type(conf_string) != str:
            raise Exception("Type error conf string")
        os.remove("conf")
        fileobj = open("conf","w")
        fileobj.write(conf_string)

        fileobj.close()
class Exporter():
    # import hashlib
    def __init__(self):
        self.pw = ""
        self.aes_obj = ""
        self.array_encrypted_jpg_list = []
        self.list_index_info = []
        self.IV = ""
        self.pw_abgleich_mit_index_fur_export = ""

    def pkdf_2(self,pw_string):
        if type(pw_string) != str:
            return Exception("pw_string type is not type str")


        bytearray_of_pw = bytearray(pw_string,"UTF-8")
        pw_deriv_counter = 0
        hashobj = hashlib.sha3_256()

        while pw_deriv_counter != 300000:
            pw_deriv_counter = pw_deriv_counter + 1
            hashobj.update(bytearray_of_pw)
            bytearray_of_pw = hashobj.digest()

            """print(rundencounter," ",pw_deriv_counter)"""
        pw_array = hashobj.digest()

        self.aes_obj = AES.new(pw_array,AES.MODE_CBC)
        self.IV = self.aes_obj.IV
        #print(self.IV)

        bytearray_of_pw = pw_array

        pw_deriv_counter = 0
        hashobj = hashlib.sha3_256()

        while pw_deriv_counter != 300000:
            pw_deriv_counter = pw_deriv_counter + 1
            hashobj.update(bytearray_of_pw)
            bytearray_of_pw = hashobj.digest()

            """print(rundencounter," ",pw_deriv_counter)"""
        self.pw_abgleich_mit_index_fur_export = hashobj.digest()


        return pw_array

    def pkdf_2_decryption(self,pw_string,IV):
        if type(pw_string) != str:
            return Exception("pw_string type is not type str")


        bytearray_of_pw = bytearray(pw_string,"UTF-8")
        pw_deriv_counter = 0
        hashobj = hashlib.sha3_256()

        while pw_deriv_counter != 300000:
            pw_deriv_counter = pw_deriv_counter + 1
            hashobj.update(bytearray_of_pw)
            bytearray_of_pw = hashobj.digest()

            """print(rundencounter," ",pw_deriv_counter)"""
        pw_array = hashobj.digest()

        self.aes_obj = AES.new(pw_array,AES.MODE_CBC,iv=IV)


        bytearray_of_pw = pw_array

        pw_deriv_counter = 0
        hashobj = hashlib.sha3_256()

        while pw_deriv_counter != 300000:
            pw_deriv_counter = pw_deriv_counter + 1
            hashobj.update(bytearray_of_pw)
            bytearray_of_pw = hashobj.digest()

            """print(rundencounter," ",pw_deriv_counter)"""
        self.pw_abgleich_mit_index_fur_export = hashobj.digest()


        return pw_array



    def encrypt_jpg(self,jpg_array):
        array = self.aes_obj.encrypt(pad(jpg_array,AES.block_size))
        self.array_encrypted_jpg_list.append(array)
        self.list_index_info.append(str(str(len(array)) + "," + str(datetime.datetime.now()) + "\n"))

    def decrypt_jpg(self,jpg_array):
        jpg_array = unpad(self.aes_obj.decrypt(jpg_array,),AES.block_size)
        #fileobj = open("beispiel.jpg","wb")
        #fileobj.write(jpg_array)
        return jpg_array

    def jpg_index_extract(self, filepath):
        try:
            fileobj = open(filepath, "r")
        except:
            raise Exception("could not open file")
        fileobj.readline()
        fileobj.readline()
        fileobj.readline()
        fileobj.readline()

        liste_index = []
        lesen = True
        while lesen == True:
            zeile = fileobj.readline()[:-1].split(",")[0]
            if len(zeile) == 0:
                break
            liste_index.append(zeile)

        return liste_index

    def video_export(self, list_filepath_indixes, pw_string,width,height,fps,name_str):

        #aes_obj.pkdf_2(pw_string)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        #width, height, fps = 2560, 1440, 10
        name_str = name_str.replace(":"," ")
        name_str = name_str.replace("_"," ")
        video = cv2.VideoWriter(("Export" + name_str + ".mp4"), fourcc, fps, (width, height))




        for i in list_filepath_indixes:
            try:
                index_liste = []
                #print(i)
                fileobj = open(i,"r")
                iv_int = fileobj.readline()
                iv = int(iv_int).to_bytes(16, "big")
                pw_user_abgleich = fileobj.readline()[1:-2]
                rtspobj = Exporter()
                fileobj.readline()
                salt = fileobj.readline()

                pw_string = pw_string + salt[:-1]

                rtspobj.pkdf_2_decryption(pw_string, iv)
                fileobj.close()
                index_liste = self.jpg_index_extract(i)

                fileobj = open(i[:-10],"rb")

                liste_encrypted_jpg = []

                if str(rtspobj.pw_abgleich_mit_index_fur_export)[2:-1] == str(pw_user_abgleich)[1:]:
                    #print("fortschritt")
                    #print(index_liste)
                    for x in index_liste:
                        liste_encrypted_jpg.append(rtspobj.decrypt_jpg(fileobj.read(int(x))))
                    fileobj.close()
                    #print(len(liste_encrypted_jpg))
                    for x in liste_encrypted_jpg:
                        image_np = numpy.frombuffer(x, numpy.uint8)
                        i = cv2.imdecode(numpy.frombuffer(image_np, dtype=numpy.uint8), cv2.IMREAD_COLOR)
                        i = cv2.resize(i, (width,height))
                        video.write(i)


            except Exception as ex:
                print(ex)
                time_str1 = str(datetime.datetime.now())
                time_str = "Error"
                error = open(time_str,"a+")
                error.write("File Error: " + str(i) + " at time: " + time_str1 + "\n")
                error.close()

        video.release()
class Haupt_ui():




    def Haupt_Seite(self,tk_main_obj):
        def start_button():
            if t_check() == False:
                textconsole.insert("1.0","Licence expiered:"+ str(global_root_t_string_ende) +"\n")
                return
            confobj = conf_datei()
            if confobj.check_for_conf() != True:
                textconsole.insert("1.0","no conf file found\n")
                return
            else:
                def pw_entry_check():
                    global prozesliste
                    pw_string = str(eingabe.get())
                    if confobj.check_if_pw_is_correct(pw_string) == True:
                        # starte hier normale function zum prozess start
                        liste_variablen_aus_conf = confobj.get_cam_info_from_config()
                        try:
                            liste_variablen_aus_conf.remove("")
                        except:
                            pass
                        if len(prozesliste) != 0:
                            try:
                                stop_button()
                            except:
                                pass


                        #static vars
                        channel_nr_str = "1"
                        stream_nr_string = "0"
                        batch_nummer = 3000
                        pipeobj = multiprocessing.Queue()
                        try:
                            while len(liste_variablen_aus_conf) != 0:
                                #print(liste_variablen_aus_conf)
                                ip_adress = liste_variablen_aus_conf[0]
                                maximaler_speicher = int(liste_variablen_aus_conf[1])
                                speicher_auflösung = (int(liste_variablen_aus_conf[2]),int(liste_variablen_aus_conf[3]))
                                username_camera = liste_variablen_aus_conf[4]
                                password_camera = liste_variablen_aus_conf[5]
                                live_resoltion_1 = liste_variablen_aus_conf[6]
                                live_resoltion_2 = liste_variablen_aus_conf[7]
                                encryption_string = liste_variablen_aus_conf[8]
                                del liste_variablen_aus_conf[:9]
                                processobj = multiprocessing.Process(target=opencamerastream,
                                                                 args=[ip_adress, username_camera, password_camera, "1", "0",
                                                                       speicher_auflösung, batch_nummer,
                                                                       pw_string, pipeobj, maximaler_speicher, live_resoltion_1, live_resoltion_2,encryption_string])
                                prozesliste.append(processobj)
                        except:
                            textconsole.insert("1.0", "There is an Error in the conf file. Please correct it\n")
                        for i in prozesliste:
                            i.start()
                        textconsole.insert("1.0", str(len(prozesliste)) + "Processes started\n" )




                    else:
                        textconsole.insert("1.0", "The password does not match the conf file information\n")

                    pw_entry_window.destroy()

                pw_entry_window = tkinter.Tk()
                label1 = tkinter.Label(pw_entry_window,text="Password")
                eingabe = tkinter.Entry(pw_entry_window)
                button_pw = tkinter.Button(pw_entry_window,text="ok",command=pw_entry_check)
                label1.grid(row=0,column=0)
                eingabe.grid(row=1,column=0)
                button_pw.grid(row=2,column=0)
        def stop_button():
            global prozesliste, que_liste
            if len(prozesliste) != 0:
                anzahl_prozesse = len(prozesliste)
                for i in prozesliste:
                    i.terminate()
                prozesliste = []
                que_liste = []
                textconsole.insert("1.0", str(anzahl_prozesse) + " Processes stopped\n")
            else:
                textconsole.insert("1.0", "No Processes to stop\n")
        def export_button():
            if t_check() == False:
                textconsole.insert("1.0","License expired:"+ str(global_root_t_string_ende) +"\n")
                return
            def export_button():
                time_str_start = str(entry_datum_start.get())
                time_str_end = str(entry_datum_ende.get())
                pw_string = entry_password.get()
                ip_str = str(entry_ip.get())
                basis_str = "./" + "records" + "/" + ip_str + "/"
                ganze_liste = os.listdir(basis_str)
                ganze_liste.sort()
                liste_nur_index = []
                for i in ganze_liste:
                    if str(i[-4:]) == "form":
                        liste_nur_index.append((str(basis_str) + str(i)))
                exportobj = Exporter()
                liste_nur_index = filtering_a_list_of_indixes_with_two_timedeltastrings(time_str_start,time_str_end,liste_nur_index)
                exportobj.video_export(liste_nur_index,pw_string,2000,1500,15,str(time_str_start + " " + time_str_end))
                textconsole.insert("1.0", "1 video was exported\n")
                export_root.destroy()

            export_root = tkinter.Tk()

            label_ip = tkinter.Label(export_root,text="IP-Adress")
            label_datum_hinweis = tkinter.Label(export_root,text="Date format 2023-01-31 14:00:00 \nYear month day hour minute second")
            label_datum_start = tkinter.Label(export_root,text="From")
            label_datum_ende = tkinter.Label(export_root,text="TilL")
            label_pasword = tkinter.Label(export_root,text="Password")
            button_export = tkinter.Button(export_root,text="Export & Decryption ",command=export_button)
            entry_ip = tkinter.Entry(export_root)
            entry_datum_start = tkinter.Entry(export_root)
            entry_datum_ende = tkinter.Entry(export_root)
            entry_password = tkinter.Entry(export_root)
            label_ip.grid(row=0,column=0)
            entry_ip.grid(row=0,column=1)
            label_datum_hinweis.grid(row=1,column=0,columnspan=2)
            label_datum_start.grid(row=2,column=0)
            entry_datum_start.grid(row=2,column=1)
            label_datum_ende.grid(row=3,column=0)
            entry_datum_ende.grid(row=3,column=1)
            label_pasword.grid(row=5,column=0)
            entry_password.grid(row=5,column=1)
            button_export.grid(row=6,column=0,columnspan=2)
            entry_ip.insert(0,"192.168.2.104")
            entry_datum_start.insert(0,"2023-02-04 14:00:00")
            entry_datum_ende.insert(0,"2023-02-04 16:00:01")
        def config_button():
            if t_check() == False:
                textconsole.insert("1.0","License expired:"+ str(global_root_t_string_ende) +"\n")
                return
            def config_set_up():
                password_string = entry_pw.get()
                confobj.create_overwririte_existingconf(password_string,[])
                textconsole.insert("1.0", "Config file saved\n")
                window_no_conf.destroy()
            def check_conf_pw():
                def change_conf_text():
                    saving_string = config_text.get("1.0",tkinter.END)
                    saving_string = saving_string[0:-1]
                    if saving_string[-1] == "\n":
                        saving_string = saving_string[0:-1]
                    os.remove("conf")
                    fileobj = open("conf","w")
                    fileobj.write(saving_string)
                    fileobj.close()
                    window_text_config_datei.destroy()
                def add_camera_to_conf():
                    def add_text_line():
                        old_str = config_text.get("1.0", tkinter.END)
                        new_str = add_camera_entry_ip.get() + "," + add_camera_entry_storage_max.get() + ","+ add_camera_entry_resolution_for_records.get() + "," + add_camera_entry_camerauser.get() + "," + add_camera_entry_camera_password.get() + "," + add_camera_entry_live_resolution.get() + "," + add_camera_entry_encryption_option.get()
                        new_str = old_str + new_str
                        config_text.delete("1.0",tkinter.END)
                        config_text.insert("1.0",new_str)
                        add_camera_window.destroy()
                    add_camera_window = tkinter.Tk()
                    label_ip = tkinter.Label(add_camera_window,text="IP Adress")
                    label_ip.grid(row=0,column=0)
                    label_storage_maximum = tkinter.Label(add_camera_window,text="Storage maximum in gigabyte")
                    label_storage_maximum.grid(row=1,column=0)
                    label_resolution_for_records = tkinter.Label(add_camera_window,text="Record resolution\n enter 0,0 for live stream only")
                    label_resolution_for_records.grid(row=2,column=0)
                    label_username = tkinter.Label(add_camera_window,text="Camera username")
                    label_username.grid(row=3,column=0)
                    label_user_pw_camera = tkinter.Label(add_camera_window,text="Camera user password")
                    label_user_pw_camera.grid(row=4,column=0)
                    label_resolution_for_live = tkinter.Label(add_camera_window,text="Resolution for Live Stream.\nInsert 0,0 to have no live stream displayed")
                    label_resolution_for_live.grid(row=5,column=0)
                    label_encryption_option = tkinter.Label(add_camera_window,text="encryption_on or encryption_off")
                    label_encryption_option.grid(row=6,column=0)

                    add_camera_entry_ip = tkinter.Entry(add_camera_window)
                    add_camera_entry_ip.insert("0","192.168.178.5")
                    add_camera_entry_ip.grid(row=0,column=1)
                    add_camera_entry_storage_max = tkinter.Entry(add_camera_window)
                    add_camera_entry_storage_max.grid(row=1,column=1)
                    add_camera_entry_resolution_for_records = tkinter.Entry(add_camera_window)
                    add_camera_entry_resolution_for_records.insert("0","1800,1200")
                    add_camera_entry_resolution_for_records.grid(row=2,column=1)
                    add_camera_entry_camerauser = tkinter.Entry(add_camera_window)
                    add_camera_entry_camerauser.grid(row=3,column=1)
                    add_camera_entry_camera_password = tkinter.Entry(add_camera_window)
                    add_camera_entry_camera_password.grid(row=4,column=1)
                    add_camera_entry_live_resolution = tkinter.Entry(add_camera_window)
                    add_camera_entry_live_resolution.insert("0","500,400")
                    add_camera_entry_live_resolution.grid(row=5,column=1)
                    add_camera_entry_encryption_option = tkinter.Entry(add_camera_window)
                    add_camera_entry_encryption_option.insert("0","encryption_off")
                    add_camera_entry_encryption_option.grid(row=6,column=1)


                    add_camera_button_add_text_line = tkinter.Button(add_camera_window,text="Add",command=add_text_line)
                    add_camera_button_add_text_line.grid(row=7,column=0,columnspan=2)

                confobj = conf_datei()
                pw_str = entry_pw.get()
                password_check.destroy()
                if confobj.check_if_pw_is_correct(pw_str) == False:
                    textconsole.insert("1.0", "Password  does not match conf file information\n")
                else:
                    window_text_config_datei = tkinter.Tk()
                    config_text = tkinter.Text(window_text_config_datei)
                    button_config_text_aktualisieren = tkinter.Button(window_text_config_datei,text="ok",command=change_conf_text)
                    button_ad_camera = tkinter.Button(window_text_config_datei,text="Add camera",command=add_camera_to_conf)
                    config_text.grid(row=0,column=0,columnspan=2)
                    button_config_text_aktualisieren.grid(row=1,column=0)
                    button_ad_camera.grid(row=1,column=1)
                    config_text.insert("1.0",confobj.get_conf_text())

            confobj = conf_datei()
            test_for_conf = confobj.check_for_conf()
            if test_for_conf == False:
                window_no_conf = tkinter.Tk()
                label_pw = tkinter.Label(window_no_conf,text="no conf file\nPassword creation")
                entry_pw =tkinter.Entry(window_no_conf)
                button_config_erstellen = tkinter.Button(window_no_conf,text="ok",command=config_set_up)
                label_pw.grid(row=0,column=0,columnspan=2)
                entry_pw.grid(row=1,column=0,columnspan=2)
                button_config_erstellen.grid(row=2,column=0,columnspan=2)

            else:
                password_check = tkinter.Tk()
                label_pw_check = tkinter.Label(password_check,text="Enter password")
                entry_pw = tkinter.Entry(password_check)
                button_conf_pwcheck = tkinter.Button(password_check,text="ok",command=check_conf_pw)
                label_pw_check.grid(row=0,column=0)
                entry_pw.grid(row=1,column=0)
                button_conf_pwcheck.grid(row=2,column=0)


        #define wigets
        textvar = "License end date\n" + str(global_root_t_string_ende)
        textconsole = tkinter.Text(tk_main_obj)
        licence_label = tkinter.Label(tk_main_obj,text=textvar)


        #label_04 = tkinter.Label(tk_main_obj)
        #label_05 = tkinter.Label(tk_main_obj)

        button_01 = tkinter.Button(tk_main_obj,text="Start",command=start_button)
        button_02 = tkinter.Button(tk_main_obj,text="Stop",command=stop_button)
        button_03 = tkinter.Button(tk_main_obj,text="Config",command=config_button)
        button_04 = tkinter.Button(tk_main_obj,text="Video Export & Decryption",command=export_button)

        #grid

        textconsole.grid(row=0,column=0,rowspan=3,columnspan=4)


        button_01.grid(row=4,column=0)
        #button_01.grid(row=4,column=0,sticky="w")
        button_02.grid(row=4,column=1)
        button_03.grid(row=4,column=2)
        #button_03.grid(row=4,column=0,sticky="e")
        button_04.grid(row=4,column=3)
        licence_label.grid(row=0,column=4)
def on_closing():
    for i in prozesliste:
        i.terminate()
    root.destroy()

if __name__ == "__main__":
    multiprocessing.freeze_support()


    uiobj = Haupt_ui()
    uiobj.Haupt_Seite(root)
    root.protocol("WM_DELETE_WINDOW",lambda :on_closing())
    root.mainloop()