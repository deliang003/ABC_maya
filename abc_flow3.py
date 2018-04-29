#coding=utf-8

#########################################
###  Mstc Alembic manager v0.1      #####
#########################################
###                                 #####
###    Author:DE_liang              #####
###                                 #####
###    Email:524707056@qq.com       #####
###                                 #####
#########################################
import sys,os,re,json
#from PySide2 import QtCore, QtGui
from PySide import QtGui ,QtCore
import maya.cmds as cmd
import pymel.core as pm
import maya.mel as mel


def maya_main_window():
    import maya.OpenMayaUI as apiUI
    from shiboken import wrapInstance
    main_win_ptr = apiUI.MQtUtil.mainWindow()
    return wrapInstance(long(main_win_ptr), QtGui.QDialog)
    
class Dialog(QtGui.QDialog):

    def __init__(self, parent=None, show=True):
        super(Dialog, self).__init__(parent=parent)
        self.tag_i=1
        self.mainLayout = QtGui.QGridLayout(self)
        self.sgOutNameGr()
        self.abcSetGr()
        self.sgOutGr()
        self.sgOutPathGr()
        self.abcInGr()
        
        self.mainLayout.addWidget(self.sg_outname_group,0,0,1,1)
        self.mainLayout.addWidget(self.sg_outpath_group,0,1,1,2)
        self.mainLayout.addWidget(self.abc_set_group,1,0,2,1)
        
        self.mainLayout.addWidget(self.sg_out_group,1,1,2,1)
        self.mainLayout.addWidget(self.abc_in_group,1,2,2,1)

        self.setLayout(self.mainLayout)

        if show:
            self.show()
            
####################################################################################
#####################       name        ##########################################
####################################################################################
    def sgOutNameGr(self):

        self.sg_outname_group= QtGui.QGroupBox("")
        self.sg_outname_labal = QtGui.QLabel("Name:")
        self.sg_name_text = QtGui.QLineEdit()

        #self.sg_path_text=QtCore.QDir.homePath()
        #self.sg_outpath_labal.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        sg_outname_layout = QtGui.QGridLayout()
        sg_outname_layout.addWidget(self.sg_outname_labal,0,0,1,1)
        sg_outname_layout.addWidget(self.sg_name_text,0,1,1,1)
        self.sg_outname_group.setLayout(sg_outname_layout)
        
####################################################################################
#####################       abc set        ##########################################
####################################################################################
    def abcSetGr(self):

        self.abc_set_group= QtGui.QGroupBox("")
        self.abc_set_start_labal = QtGui.QLabel("start:")
        self.abc_set_end_labal = QtGui.QLabel("end:")
        self.abc_set_start_text = QtGui.QLineEdit("1")
        self.abc_set_end_text = QtGui.QLineEdit()

        #self.sg_path_text=QtCore.QDir.homePath()
        #self.sg_outpath_labal.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        abc_set_layout = QtGui.QGridLayout()
        abc_set_layout.addWidget(self.abc_set_start_labal,0,0,1,1)
        abc_set_layout.addWidget(self.abc_set_start_text,0,1,1,1)
        
        abc_set_layout.addWidget(self.abc_set_end_labal,1,0,1,1)
        abc_set_layout.addWidget(self.abc_set_end_text,1,1,1,1)
        self.abc_set_group.setLayout(abc_set_layout)


        
####################################################################################
#####################       PATH        ##########################################
####################################################################################

    def sgOutPathGr(self):

        self.sg_outpath_group= QtGui.QGroupBox("")
        self.sg_outpath_labal = QtGui.QLabel("PATH:")
        self.sg_path_text = QtGui.QLineEdit()
        self.sg_search_labal = QtGui.QPushButton("Search...")
        #self.sg_path_text=QtCore.QDir.homePath()
        #self.sg_outpath_labal.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        sg_outpath_layout = QtGui.QGridLayout()
        sg_outpath_layout.addWidget(self.sg_outpath_labal,0,0,1,1)
        sg_outpath_layout.addWidget(self.sg_path_text,0,1,1,2)
        sg_outpath_layout.addWidget(self.sg_search_labal,0,3,1,1)
        self.sg_outpath_group.setLayout(sg_outpath_layout)
        self.connect(self.sg_search_labal, QtCore.SIGNAL('clicked()' ), self.setPathFn )

    def setPathFn(self):
        out_dir = QtCore.QDir.toNativeSeparators(QtGui.QFileDialog.getExistingDirectory(self,'璇锋覆鏌撹矾寰..',QtCore.QDir.currentPath()))
        
        print out_dir
        #out_dir = QtGui.QFileDialog.getExistingDirectory(self,'璇锋覆鏌撹矾寰..',QtCore.QDir.currentPath())
        self.sg_path_text.setText(out_dir)
####################################################################################
#####################       SG OUT        ##########################################
####################################################################################
       
    def sgOutGr(self):

        self.sg_out_group= QtGui.QGroupBox("")
        self.sg_out_btn = QtGui.QPushButton('Abc OUT')
        self.sg_out_btn.setStyleSheet("background-color: rgb(170, 0, 255);min-height:60;font: bold 18px;")
        sg_out_layout = QtGui.QGridLayout()
        sg_out_layout.addWidget(self.sg_out_btn,0,0,1,1)
        self.sg_out_group.setLayout(sg_out_layout)
        self.connect(self.sg_out_btn, QtCore.SIGNAL('clicked()' ), self.cleaneNamceSpace)
# 0
    def cleaneNamceSpace(self):
        
        mel.eval("MLdeleteUnused;")
        allNodes = pm.ls()  
        
        for node in allNodes:
               
            buffer= node.name() 
            try:
                newName = buffer.split(':')[-1]  
                pm.rename (node,newName)  
            except:
                pass
        self.similarNameFixFn() 
        
    def similarNameFixFn(self):
        
        obj = pm.ls(sl=1,sn=1,transforms=1)
        namespece=[]
        for i in obj:
            namespece.append(i.split("|")[-1])
            subl=[i for i in namespece if namespece.count(i)>1]

            new_nameSpace=set(subl)
        for i in obj:
            print i.name()
            if i.name().split("|")[-1] in new_nameSpace:
                self.tag_i+=self.tag_i
                newName = i.name().split("|")[-1]+str(self.tag_i)+"_tm"
                #print newName
                newNameShape = newName+"Shape"
                pm.rename (i,newName) 
                pm.rename (pm.listRelatives(i)[0].name(),newNameShape)
            else:
                newNameShape = i.name()+"Shape"
                pm.rename (pm.listRelatives(i)[0].name(),newNameShape) 
        self.abcOut() 
                  
#    1 
    def abcOut(self):
        name = self.sg_name_text.text()
        path = self.sg_path_text.text()
        self.absolute_path = path+'\\'+name
        
        start = self.abc_set_start_text.text()
        if  self.abc_set_end_text.text():
            end = self.abc_set_end_text.text()
            
            
        else:
            self.errorFn()
        out_mesh = cmds.ls(sl=1,transforms=1)
        root=""
        for i in range(0,len(out_mesh)):
            
            root+=str(" "+"-root"+" "+out_mesh[i])
        print root
        save_name = self.absolute_path+'.abc'
        command = "-frameRange " + start + " " + end +" -uvWrite -worldSpace " + root + " -file " + save_name
        cmd.AbcExport ( j = command )
        print "abc is exprot .........Please waitting json"

        self.jsOutFn()
# 2       
    def jsOutFn(self):

        obj_sg_data = {}
        self.all_sg =[]
        self.abc_obj = pm.ls(sl=1,dag=1,type='mesh')
        for i in self.abc_obj: 
            i_seluvs = pm.polyEvaluate(i,uvs=1 )    
            sg=i.outputs()
            for s in set(sg):
                if isinstance( s, pm.nodetypes.ShadingEngine):
                    if s.name()=='initialShadingGroup':
                        pass
                    else:
                        self.all_sg.append(s)
                        try:
                            obj_sg_face = pm.sets(s,q=True)
                            print s.name()
                            face =[]
                #print obj_sg_face

                            for i in obj_sg_face:
                
                    #print i.name()
                                face.append(i.name())
                #print face

                            obj_sg_data[s.name()]=face
                            with open(self.absolute_path+'.json', 'w') as outfile:
                                json.dump(obj_sg_data, outfile, sort_keys=True, indent=4, ensure_ascii=False)
                            outfile.close()
                        except:
                            pass
                else:
                    pass
        print "json is ok .........Please waitting shader"
        self.sgOutFn()
#  3  
    def sgOutFn(self):
        pm.select(self.all_sg,r=1,noExpand=1)
        cmd.file(self.absolute_path+"_shader.ma", op='', f=True, typ='mayaAscii', pr=True, es=True)
        #pm.select(self.abc_obj)
        #self.sg_out = cmd.exportEdits(self.absolute_path,type='editMA',selected=1,includeShaders=1)
        print "shader is out"  
        print "Abc Export Successful........"      
# 4
    def errorFn(self):
        
        print "Please SET Frame Range"

####################################################################################
#####################       name        ##########################################
####################################################################################

    def abcInGr(self):

        self.abc_in_group= QtGui.QGroupBox("")
        self.abc_in_btn = QtGui.QPushButton("Abc  IN")
        self.abc_in_btn.setStyleSheet("background-color: rgb(17, 98, 39);min-height:60;font: bold 18px")
        #self.sg_path_text=QtCore.QDir.homePath()
        #self.sg_outpath_labal.setFrameStyle(QtGui.QFrame.StyledPanel|QtGui.QFrame.Sunken)
        abc_in_layout = QtGui.QGridLayout()
        abc_in_layout.addWidget(self.abc_in_btn,0,0,1,1)
        self.abc_in_group.setLayout(abc_in_layout)
        self.connect(self.abc_in_btn, QtCore.SIGNAL('clicked()' ), self.abcInFn )
        
    def abcInFn(self):
        name = self.sg_name_text.text()
        path = self.sg_path_text.text()
        self.absolute_path = path+'\\'+name
        cmd.file( self.absolute_path+"_shader.ma", i=True, applyTo=":")
        print "shader is in"
        cmd.file( self.absolute_path+".abc", i=True, applyTo=":")
        print "abc is in"

        #dir_file = open('D:\CS\cs_he\ca.json', 'r')
        dir_file = open(self.absolute_path+'.json', 'r')
        sg_file = json.load(dir_file)
        print "json is load"
        for i in sg_file:
            for f in sg_file[i]: 
                try:
                    
                    print f          
                    cmd.select(f)
                except:
                    print "no"
                    pass
                else:
                    cmd.hyperShade( assign=i )

        dir_file.close()
        print "Abc Is In"

 
def maya_ui():
    
    dialog = Dialog(parent=maya_main_window()) 
    dialog.setWindowTitle("Alembic Manager")  

if __name__ == '__main__':
    maya_ui()


