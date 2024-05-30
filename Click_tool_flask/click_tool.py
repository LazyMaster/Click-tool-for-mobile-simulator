#NOX模擬器用 pyautogui工具 
import pynput
import threading
import pyautogui as pag
import time
import os.path


pag.FAILSAFE = False

def on_press(key):
    pass

def is_pass(key):
    if key == pynput.keyboard.Key.pause:
        # Stop listener
        return False
def is_esc(key):
    if key == pynput.keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released

    
    
def wait_for_pass():
    with pynput.keyboard.Listener(
            on_press=on_press,
            on_release=is_pass) as listener:
        try :
            listener.join()
        except:
            pass
def wait_for_esc():
    with pynput.keyboard.Listener(
            on_press=on_press,
            on_release=is_esc) as listener:
        try :
            listener.join()
        except:
            pass

def wait_any_key(t):
    with pynput.keyboard.Events() as events:
        # Block at most one second
        event = events.get(t)
        if event is None:
            pass
        else:
            wait_for_esc()

def keyboard_wait(t):
    with pynput.keyboard.Events() as events:
        # Block at most one second
        event = events.get(t)
        if event is None:
            return False
        else:
            return True
        


class click_tool():
    def __init__(self,debug=False ,leftup_pic = False):
        self.leftup_pic = leftup_pic
        if leftup_pic:
            self.wait_True(self.locate_leftup)
        else:
            self.leftup=(0,0)
        self.debug = debug
        self.picdir = ''
        self.def_reg= (0,0,1600,900)
        self.pause= False
        self.wait_pause_thread()
        self.conf = 0.9

        self.pic_reg_dict = dict()
    def reset_nox(self):
        time.sleep(2)
        self.click_im('quit.png',reg=(0,0,1680,900))
        time.sleep(10)
    def locate_leftup(self):
        try:
            box = pag.locateOnScreen(self.leftup_pic)
            self.leftup = (box[0],box[1]+box[3])
            return True
        except:
            return False
        
    def wait_pause_thread(self):
        def wait_pause():
            while True:
                wait_for_pass()
                self.pause = not self.pause
                time.sleep(1)
        threading.Thread(target=wait_pause).start()
        
    def stop(self):
        while self.pause:
            time.sleep(0.5)


            
    def search_all(self,image,region=None):
        if region == None:
            region = self.def_reg
        image = os.path.join(self.picdir,image)
        return list(pag.locateAllOnScreen(image,region=(self.leftup[0]+region[0],self.leftup[1]+region[1],region[2],region[3]), confidence=self.conf))
    def search_im(self,image,region=None):
        if region == None:
            if image in self.pic_reg_dict:
                region = self.pic_reg_dict[image]
            region = self.def_reg
        image_d = os.path.join(self.picdir,image)
        
        box = pag.locateOnScreen(image_d,region=(self.leftup[0]+region[0],self.leftup[1]+region[1],region[2],region[3]), confidence=self.conf)
        if self.debug and box != None:
            print('\'' + image + '\':' ,(box[0] - self.leftup[0] , box[1] - self.leftup[1] , box[2],box[3]))
        return box
    def get_im_left_up(self,image,region=None):
        if region == None:
            region = self.def_reg
        box = self.search_im(image,region=region)
        if box == None:
            return False
        return (box[0] - self.leftup[0] , box[1] - self.leftup[1])

    def is_im(self,image,region=None):
        if region == None:
            region = self.def_reg
        return not self.search_im(image,region=region) == None
    def count_im(self,image,region=None):
        if region == None:
            region = self.def_reg
        return len(self.search_all(image,region=region))
    def offsetcoord(self,coodi):
        return (coodi[0]+self.leftup[0],coodi[1]+self.leftup[1])
    
    def click(self,*coodi,**arg):
        self.stop()
        pag.mouseUp(button='left')
        p = pag.position()
        try:
            pag.click(self.offsetcoord(coodi[0]),**arg)
        except:
            pag.click()
        pag.moveTo(p)
        return None
    def just_click(self,*coodi,**arg):
        self.stop()
        pag.click()
        return None
    
    def drag_mouse(self,start_point, end_point, steps=10, delay=0.05):
        # Calculate the change for each step
        start_point = self.offsetcoord(start_point)
        end_point   = self.offsetcoord(end_point)
        dx = (end_point[0] - start_point[0]) / steps
        dy = (end_point[1] - start_point[1]) / steps
        
        # Move to the starting point
        pag.moveTo(start_point[0], start_point[1])
        
        # Press the left mouse button down
        pag.mouseDown()
        
        # Loop over each step
        for step in range(1, steps + 1):
            # Calculate the new position
            new_x = start_point[0] + dx * step
            new_y = start_point[1] + dy * step

            # Move the mouse to the new position
            pag.moveTo(new_x, new_y)
            
            # Wait for the delay time
            time.sleep(delay)
        
        # Release the left mouse button
        pag.mouseUp()


    
    def click_im(self,im,reg=None):
        self.stop()
        if reg == None:
            reg = self.def_reg
        box = self.search_im(im,region=reg)
        if box == None:
            return False
        else:
            pag.click((box[0],box[1]))
            return True
    def click_until_True(self,pt,function,target):
        for i in range(100):
            self.click(pt)
            if function(target):
                break
            time.sleep(0.5)
    
    def click_im_until_disappear(self,im,reg=None):
        if reg == None:
            reg = self.def_reg
        if self.is_im(im,region=reg):
            for i in range(20):
                if not self.click_im(im,reg=reg):
                    return True
                time.sleep(1)
        return False
    def click_pt_until_im_disappear(self,pt,im,reg=None,delay = 1):
        if reg == None:
            reg = self.def_reg
        if self.is_im(im,region=reg):
            for _ in range(10):
                self.click(pt)
                time.sleep(delay)
                if not self.is_im(im,region=reg):
                    return True
        return False
    def wait_True(self,function,*target,times=100):
        #wait_True(self,function)
        for i in range(times):
            isreturn = False
            if function(*target):
                return True
            time.sleep(1)
        return False
    def wait_im(self,*im,times=100):
        if len(im) > 1:
            def conbine(*a):
                return True in [self.is_im(image) for  image in a]
            return self.wait_True(conbine,*im,times=times)
        else:
                
            return self.wait_True(self.is_im,*im,times=times)
    def scroll_down_slowly(self,steps=10, delay=0.1):
        for _ in range(steps):
            pag.scroll(-1)  # 每次只滾動一步
            time.sleep(delay)  # 等待延遲時間

class fgo(click_tool):
    def __init__(self,**combat_dict):
        super().__init__(self,leftup_pic = 'nox_leftup.png')
        self.d = {
            'situation'          :0 ,
            'round'              :0 ,
            'round_skills_use'   :[[1,1,1,1,1,1,1,1,1],
                                   [1,1,1,1,1,1,1,1,1],
                                   [1,1,1,1,1,1,1,1,1]],
            'round_skills_target':[[0,0,0,0,0,0,0,0,0],
                                   [0,0,0,0,0,0,0,0,0],
                                   [0,0,0,0,0,0,0,0,0]],
            'round_artifa_use'   :[[1,1,1],
                                   [1,1,1],
                                   [1,1,1]],
            'round_cloth_use'   :[[0,0,0],
                                  [0,0,0],
                                  [0,0,0]],
            'round_target'       :[0,0,0],
            'skill_istar'        :0,
            'skill_emiya'        :0,
            'weak_score'         :1,
            'resist_score'       :-1,
            'play_times'         :1,
            'apple_eat'          :0,
                                  #0:NO 1:銅 2:銀 3:金
            'apple_eat_limit'    :100,
            'event_item'         :0,
                                  #0:NO 1:item1
            'battle_repeat'      :True,
            'log'                :False,
            'support_servant'    :False,
            'support_servant_2'  :False,
            'artifact_bake'      :False,
            
        }
        self.d.update(combat_dict)
        if self.d['log'] :
            for k in self.d.keys():
                print('{}: {}'.format(k.ljust(20),self.d[k]))
        
        
        self.picdir = 'Fgo'
        self.debug = False
        self.pic_reg_dict ={
            'cloth_buttom.png':(1463, 356, 63, 79),
            'skill_choose.png':(733, 231, 151, 21),
            'is_battle_end_repeat.png':(966, 684, 196, 41)
        }

    def update_d(self,dic):
        self.d.update(dic)
    def combat(self,funcs_with_args_1=[],funcs_with_args_2=[],funcs_with_args_3=[],IsOneTime = False,start_end = False):
        times = 0
        result = 'NO RESULT'
        is_start = True
        while True:
            time.sleep(1)
            if self.is_im('cloth_buttom.png') or self.is_im('cloth_buttom2.png'):
                if start_end and times:
                    break
                if self.round_update():
                    self.use_cloth_list()
                    if self.d['round'] == 1:
                        for func, args, kwargs in funcs_with_args_2:
                            func(*args, **kwargs)
                        self.change_target()
                    if self.d['round'] == 2:
                        for func, args, kwargs in funcs_with_args_3:
                            func(*args, **kwargs)
                        self.change_target()
                if is_start and self.d['round'] == 0:
                    time.sleep(3)
                    for func, args, kwargs in funcs_with_args_1:
                        func(*args, **kwargs)  # 傳遞參數到每個func
                    is_start = False
                    self.change_target()
                
                self.use_skill_list()
                self.attack()
                if IsOneTime:
                    break

                        
            elif self.is_im('is_battle_end.png'):
                is_start = True
                times += 1
                print('Turn {} end'.format(times))
                if times >= self.d['play_times']:
                    result ='play times end' 
                    break
                if self.battle_end() == 'NoAp':
                    result ='NoAp END'
                    break
            elif self.click_im('ctd_1.png'):
                for i in range(100):
                    self.click_im('ctd_1.png')
                    self.click((300,50))
                    if self.click_im('ctd_2.png'):
                        break
                    time.sleep(3)
                
        print(result)

                
    def change_target(self):
        if self.d['round_target'][self.d['round']] < 0:
            return False
        self.wait_im('cloth_buttom.png')
        target_list= [(700-300*i,50 ) for i in range(3)]
        self.click(target_list[self.d['round_target'][self.d['round']]])
        time.sleep(1)
        self.click((1000,50))
        time.sleep(2)
        
    def battle_end(self):
        for i in range(100):
            time.sleep(1)
            self.click((300,50))
            if self.is_im('is_battle_end_repeat.png'):
                if self.d['battle_repeat']:
                    self.click((1055,700))
                else:
                    self.click((500,700))
                    
            elif self.is_im('is_battle_end_confilm.png'):
                self.click((1385,842))
            elif self.is_im('is_eat_apple.png'):
                if self.d['apple_eat_limit'] == 0:
                    self.d['apple_eat'] = 0
                
                if self.d['apple_eat'] == 0:
                    return 'NoAp'
                else:
                    self.d['apple_eat_limit'] -= 1
                if self.d['apple_eat'] == 3:
                    self.click((817 ,424))
                if self.d['apple_eat'] == 2:
                    self.click((810 ,599))
                if self.d['apple_eat'] == 1:
                    self.click((845 ,707))
                if self.d['apple_eat'] == -1:
                    self.click((1269 ,656))
                    time.sleep(1)
                    self.click((845 ,707))
                
                time.sleep(1)
                self.click_im('is_eat_apple_confilm.png')
            elif self.is_im('is_battle_end_menu.png'):
                self.click((1100 ,230))
            elif self.is_im('is_support.png'):
                self.battle_start()
                return 'battle_end'
            self.click_im('is_battle_end_reject_friend.png')
    def battle_start(self):
        localv1 = True# 
        Flow_time = 0
        while True:
            time.sleep(1)
            if localv1 and self.is_im('is_support.png'):
                time.sleep(2)
                if self.d['support_servant_2']:
                    leftup = self.get_im_left_up(self.d['support_servant_2'])
                    if leftup and self.click_im(self.d['support_servant'],reg=(0,leftup[1]-150,1600,300)):
                        time.sleep(3)
                        localv1 = False
                    
                elif self.d['support_servant']:
                    if self.click_im(self.d['support_servant']):
                        time.sleep(3)
                        localv1 = False
                elif self.click_pt_until_im_disappear((360,360),'is_support.png',delay=3):
                        localv1 = False
                if localv1:
                    #查找失敗
                    if Flow_time < 10:
                        self.drag_mouse((621,630),(621,380))
                        Flow_time += 1
                    else:
                        Flow_time = 0
                        self.click_im('is_support.png')
                        time.sleep(3)
                        self.click_im('battle_start_surpport_reflesh_2.png')
            elif self.is_im('battle_start_ispartychoose.png'):
                self.click((1500,850))
                time.sleep(1)
                if not self.is_im('battle_start_ispartychoose.png'):
                    if self.is_im('battle_start_event_item.png'):
                        event_items_list = [(1000,825) , (800,250)]
                        #                   don't use    item1
                        if self.click_pt_until_im_disappear(event_items_list[self.d['event_item']],
                                                            'battle_start_event_item.png'):
                            break
                        else:
                            self.click_pt_until_im_disappear(event_items_list[0],'battle_start_event_item.png')
                            break
                    break
            elif self.is_im('cloth_buttom.png') or self.is_im('cloth_buttom2.png') or self.is_im('ctd_1.png'):
                break
                
            
                       

        
    def round_update(self):
        #return true if round change
        pic_list = ['round_1.png','round_2.png','round_3.png']
        for i in range(3):
            if self.is_im(pic_list[i],region=(1103,12,30,40)):
                if self.debug:
                    print('round : ',i)
                if self.d['round'] != i:
                    self.d['round'] = i
                    return True
                else:
                    return False
                
            
        
    def use_cloth_list(self):
        sl =self.d['round_cloth_use'][self.d['round']]
        for i in range(3):
            if sl[i]:
                self.use_cloth_skill(i)
    def use_skill_list(self,skills_list=False,target_list=False):
        if not skills_list:
            sl =self.d['round_skills_use'][self.d['round']]
        else:
            sl = skills_list
        if not target_list:
            target_list =self.d['round_skills_target'][self.d['round']]

        for i in range(9):
            if sl[i]:
                self.use_skill(i,target=target_list[i])
    def friendship_gacha(self):
        while True:
            if self.click_im('fp_gach2.png') or self.click_im('fp_gach1.png'):
                pass
            else:
                self.click((300,50))
            time.sleep(1)
    def use_cloth_skill(self,n,target=0,target2 = 3):
        self.wait_im('cloth_buttom.png')
        skill_list = [(1131+i*111 ,392) for i in range(3)]
        target_list= [(418+ i*400 ,552) for i in range(3)]
        change_servert_list = [(170+i*250,440) for i in range(6)]
        
        self.click_im('cloth_buttom.png')
        time.sleep(1)
        self.click(skill_list[n])
        time.sleep(1)
        if self.is_im('skill_choose.png'):
            self.click(target_list[target])
        if self.is_im('battle_is_servant_change.png'):
            self.click(change_servert_list[target])
            time.sleep(1)
            self.click(change_servert_list[target2])
            time.sleep(1)
            self.click((800,780))
    def use_skill(self,n,target=0):
        self.wait_im('cloth_buttom.png')
        if self.debug:
            print('use_skill(self,{},target={})'.format(n,target))
        skill_list = [(48 + i*397 + j*117, 683) for i in range(3) for j in range(3)]
        target_list= [(418+ i*400 ,552) for i in range(3)]
        
        target_list_2 = [(600,550),(1000,550)]
        x , y = skill_list[n]
        if not self.is_im('skill_used.png',region =(x-15,y+62 ,90,40)):
            self.click((x+45,y+45))
            time.sleep(0.5)
            if self.is_im('skill_choose.png'):
                self.click(target_list[target])
            elif self.is_im('skill_istar.png'):
                self.click(target_list[self.d['skill_istar']])
            elif self.is_im('skill_istar2.png'):
                self.click(target_list[self.d['skill_istar']])
            elif self.is_im('skill_emiya.png'):
                self.click(target_list_2[self.d['skill_emiya']])
            elif self.is_im('skill_cancel.png'):
                self.click((524,531))
            elif self.is_im('skill_charinfo.png'):
                self.click((1500,600))
            self.click_im('skill_NPnoenough.png')
            time.sleep(0.2)
            self.click((50,300))
    def attack(self,an=False,artifa=False):
        card_area = [(0 + 320*i,400,340,500) for i in range(5)]
        card_list = [(160 + 320*i,600) for i in range(5)]
        artifact_list = [(500,160),(800,160),(1100,160)]
        
        
        #---------------enter---------------------
        self.wait_im('cloth_buttom.png')
        time.sleep(1)
        self.click((1420,736))
        time.sleep(2)
        #---------------score---------------------
        card_score = [0,]*5
        im_score_map = {
            'card_weak.png' : self.d['weak_score'],
            'card_resist.png' : self.d['resist_score'],
            'card_cantmove.png' : -10
        }
        for im in im_score_map.keys():
            for area in range(5):
                if self.is_im(im ,region=card_area[area]):
                    card_score[area] += im_score_map[im]
                    
        #sort
        if self.debug:
            print('card_score :{}'.format(card_score))
        slist=[ i[1] for i in sorted(zip(card_score,range(5) ), reverse=True) ]
        if self.debug:
            print('card_order :{}'.format(slist))
        #---------------click---------------------
        if not artifa:
            artifa = self.d['round_artifa_use'][self.d['round']]
            
        
        if an or self.d['artifact_bake']:
            for i in [2,1,0]:
                if artifa[i]:
                    time.sleep(0.5)
                    self.click(artifact_list[i])
                    time.sleep(0.5)
                    self.click_im('battle_arti_break.png')
        else:
            for i in range(3):
                if artifa[i]:
                    time.sleep(0.5)
                    self.click(artifact_list[i])
                    time.sleep(0.5)
                    self.click_im('battle_arti_break.png')
            
        
        for i in slist:
            time.sleep(0.5)
            self.click(card_list[i])
        
        
    def gift(self):
        for i in range(1000):
            time.sleep(0.1)
            if self.click_im('gift.png') or self.click_im('gift_2.png') :
                for i in range(5000):
                    time.sleep(1)
                    self.click()
                    pag.click()
            if self.click_im('gift_reset.png'):
                time.sleep(5)
                self.click_im('gift_reset2.png')
                time.sleep(5)
                self.click_im('gift_reset3.png')
    def gifbox_take(self,limit,times_limit=300):
        #gifbox_take(limit:TAKE AMOUNT <= limit   times_limit=300):
        count = 0
        times = 0
        while True:
            pic_list = ['giftbox_x1.png','giftbox_x2.png','giftbox_x3.png'][0:limit]
            time.sleep(1)
            if True not in map(self.click_im , pic_list):
                pag.moveTo(self.offsetcoord((500,800)))
                pag.drag(0, -300, 1 , button='left')
                count += 1
            else:
                count = 0
                times +=1
            if self.is_im('item_full.png') or count > 10 or times >= times_limit:
                break
                
    def skill_levelup(self,times):
        for i in range(times):
            while True:
                if self.click_im('skill_enhance.png'):
                    time.sleep(2)
                    self.click_im('skill_enhance_2.png')
                    time.sleep(2)
                    self.click_until_True((500,100),self.is_im,'skill_enhance.png')
                    break
    #------------------------------------------------------------------
        


