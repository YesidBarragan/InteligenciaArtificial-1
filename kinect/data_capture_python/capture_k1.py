import rospy
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
import struct
import ctypes
import time, os, sys

path_data = os.getcwd() + "/data/raw"
flag=0

def saveCloud_txt(fileName):
    fileName= fileName + "_" + time.strftime("%d-%m-%y")+'-'+time.strftime("%I-%M-%S")
    completeName = os.path.join(path_data, fileName + '.txt')
    f = open(completeName,"a") #opens file with name of "[fileName].txt"
    dataFile= "%" + "X"+"\t"+ "Y"+"\t"+  "Z" +"\t"+ "R" +"\t" + "G"+"\t"+ "B" + "\n"
    f.write(dataFile)
    return f

def callback(data):
    global flag
    rospy.loginfo('Data acquiring')
    pc = pc2.read_points(data,skip_nans=True)
    int_data=list(pc)
    for P in int_data:
	x=P[0]
	z=-P[1]
	y=P[2]
	s=struct.pack('>f', P[3])
	i=struct.unpack('>l',s)[0]
	pack = ctypes.c_uint32(i).value
	R=(pack & 0x00FF0000)>> 16
	G=(pack & 0x0000FF00)>> 8
	B=(pack & 0x000000FF)
	dataFile = str(x)+"\t"+ str(y)+"\t"+ str(z) +"\t"+ str(R)+"\t" +str(G) +"\t"+ str(B)+ "\n"
	f.write(dataFile)
    	print "X: "+str(x)+ "; Y: "+str(y)+"; Z: "+str(z) +"; R: "+str(R)+" ; G:"+str(G)+"; B:"+str(B)
	del x,y,z,R,G,B
    print "--------------------------------------------------------------------------------------------"
    flag=1

def ros_listener():
    global flag
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('Kinect_Capture', anonymous=True)
    rospy.Subscriber('/camera/depth_registered/points', PointCloud2, callback)
    while flag==0:
	nop_op = 0
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

if __name__ == '__main__':
    fileName = raw_input('File name: ')
    print "5"
    time.sleep(1)
    print "4"
    time.sleep(1)
    print "3"
    time.sleep(1)
    print "2"
    time.sleep(1)
    print "1"
    time.sleep(1)
    f = saveCloud_txt(fileName)
    ros_listener()
