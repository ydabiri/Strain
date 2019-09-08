#Copyright@Yaghoub Dabiri, ydabiri@gmail.comment
#Any usage, modification or distribution without Yaghoub Dabiri's ermission (ydabiri@gmail.com) is forbidden.
import os
import odbAccess
from odbAccess import *
from abaqusConstants import *
import string
from collections import OrderedDict
import math


odb = openOdb(path='odb_file.odb')

Ring_nodes = odb.rootAssembly.instances['PART-1-1'].nodeSets['LV-RING']
Endo_nodes = odb.rootAssembly.instances['PART-1-1'].nodeSets['ENDO-NODES']
Annulus_center = odb.rootAssembly.instances['PART-1-1'].nodeSets['LV-RP']
coords_ed = odb.steps['Beat1'].frames[0].fieldOutputs['COORD']
coords_es = odb.steps['Beat1'].frames[5].fieldOutputs['COORD']


node_data_ring_ed = coords_ed.getSubset(region=Ring_nodes)
node_data_ring_es = coords_es.getSubset(region=Ring_nodes)

node_data_endo_ed = coords_ed.getSubset(region=Endo_nodes)
node_data_endo_es = coords_es.getSubset(region=Endo_nodes)

node_data_Annulus_center_ed = coords_ed.getSubset(region=Annulus_center)
node_data_Annulus_center_es = coords_es.getSubset(region=Annulus_center)

#In this section the circumferential strain is calculated
########################################################################
#The annulus ring length for end diastole is calculated Here
counter0 = 0
length_ring_ed = 0.0
previous_node1_x =  0.0
previous_node1_y =  0.0
previous_node1_z =  0.0
for node1 in node_data_ring_ed.values:
    node_label_node1 = node_data_ring_ed.values[counter0].nodeLabel
    node_coordinate_node1 = node_data_ring_ed.values[counter0].data
#    print 'node_label_node1=',node_label_node1
#    print 'node_coordinate_node1=',node_coordinate_node1
    if counter0==0:
        previous_node1_x =  node_coordinate_node1[0]
        previous_node1_y =  node_coordinate_node1[1]
        previous_node1_z =  node_coordinate_node1[2]
    else:
        delta_length = math.sqrt((node_coordinate_node1[0] - previous_node1_x)**2 + (node_coordinate_node1[1]-previous_node1_y)**2 + (node_coordinate_node1[2]-previous_node1_z)**2)
        length_ring_ed = length_ring_ed + delta_length

    counter0 = counter0 + 1

#print 'ed_length =', length_ring_ed
######################################################################
#The annulus ring length for end systole is calculated Here
counter1 = 0
length_ring_es = 0.0
previous_node2_x =  0.0
previous_node2_y =  0.0
previous_node2_z =  0.0
for node2 in node_data_ring_es.values:
    node_label_node2 = node_data_ring_es.values[counter1].nodeLabel
    node_coordinate_node2 = node_data_ring_es.values[counter1].data
    #print 'node_label_node2=',node_label_node2
    #print 'node_coordinate_node2=',node_coordinate_node2
    if counter1==0:
        previous_node2_x =  node_coordinate_node2[0]
        previous_node2_y =  node_coordinate_node2[1]
        previous_node2_z =  node_coordinate_node2[2]
    else:
        delta_length2 = math.sqrt((node_coordinate_node2[0] - previous_node2_x)**2 + (node_coordinate_node2[1]-previous_node2_y)**2 + (node_coordinate_node2[2]-previous_node2_z)**2)
        length_ring_es = length_ring_es + delta_length2

    counter1 = counter1 + 1

#print 'ed_length =', length_ring_es

circumferential_strain = 100*(length_ring_es-length_ring_ed)/length_ring_ed

print 'circumferential_strain =',circumferential_strain

########################################################################
#In this section the radial strain is calculated
########################################################################
#In this section the mean radial distance at end diastole is calculated
center_node_label_ed = node_data_Annulus_center_ed.values[-1].nodeLabel
previous_node3_coordinates_ed = node_data_Annulus_center_ed.values[-1].data
previous_node3_x =  previous_node3_coordinates_ed[0]
previous_node3_y =  previous_node3_coordinates_ed[1]
previous_node3_z =  previous_node3_coordinates_ed[2]

counter2 = 0
length_radial_ed = 0.0
for node3 in node_data_ring_ed.values:
    node_label_3 = node_data_ring_ed.values[counter2].nodeLabel
    node_coordinate_3 = node_data_ring_ed.values[counter2].data
#    print 'node_label_3=',node_label_3
#    print 'node_coordinate_3=',node_coordinate_3
    radial_length_node_ed = math.sqrt((node_coordinate_3[0] - previous_node3_x)**2 + (node_coordinate_3[1]-previous_node3_y)**2 + (node_coordinate_3[2]-previous_node3_z)**2)
    length_radial_ed = length_radial_ed + radial_length_node_ed
#    print counter2
    counter2 = counter2 + 1


#print 'counter2 =',counter2
#print 'ed_length =', length_radial_ed
length_radial_mean_ed = length_radial_ed/counter2
print 'radial_length_ed =',length_radial_mean_ed
##########################################################################
##In this section the mean radial distance at end systole is calculated
center_node_label_es = node_data_Annulus_center_es.values[-1].nodeLabel
previous_node4_coordinates = node_data_Annulus_center_es.values[-1].data
previous_node4_x =  previous_node4_coordinates[0]
previous_node4_y =  previous_node4_coordinates[1]
previous_node4_z =  previous_node4_coordinates[2]

counter3 = 0
length_radial_es = 0.0
for node4 in node_data_ring_es.values:
    node_label_4 = node_data_ring_es.values[counter3].nodeLabel
    node_coordinate_4 = node_data_ring_es.values[counter3].data
#    print 'node_label_4=',node_label_4
#    print 'node_coordinate_4=',node_coordinate_4
    radial_length_node_es = math.sqrt((node_coordinate_4[0] - previous_node3_x)**2 + (node_coordinate_4[1]-previous_node3_y)**2 + (node_coordinate_4[2]-previous_node3_z)**2)
    length_radial_es = length_radial_es + radial_length_node_es
#    print counter3
    counter3 = counter3 + 1


#print 'counter3 =',counter3
#print 'es_length =', length_radial_es
length_radial_mean_es = length_radial_es/counter3
print 'radial_length_es =',length_radial_mean_es


strain_radial = 100*(length_radial_mean_es - length_radial_mean_ed)/length_radial_mean_ed

print 'strain_radial =',strain_radial

#In this section the longitudinal strain is calculated
##############################################################
#In this section the ed longitunial strain is calculaed
distance_max_long_axis_ed = 0.0
first_point_long_axis_ed = 0
second_point_long_axis_ed = 0

counter4 = 0
for node5 in node_data_Annulus_center_ed.values:
    node_label_5 = node_data_Annulus_center_ed.values[counter4].nodeLabel
    node_coordinate_5 = node_data_Annulus_center_ed.values[counter4].data
    counter4 = counter4 + 1

    counter5 = 0
    for node6 in node_data_endo_ed.values:
        node_label_6 = node_data_endo_ed.values[counter5].nodeLabel
        node_coordinate_6 = node_data_endo_ed.values[counter5].data
        if (node_label_5 != node_label_6):
            distance_long_axis_ed = math.sqrt((node_coordinate_5[0] - node_coordinate_6[0])**2 + (node_coordinate_5[1]-node_coordinate_6[1])**2 + (node_coordinate_5[2]-node_coordinate_6[2])**2)

            if (distance_long_axis_ed > distance_max_long_axis_ed):
                distance_max_long_axis_ed = distance_long_axis_ed
                first_point_long_axis_ed = node_label_5
                second_point_long_axis_ed = node_label_6
        counter5 = counter5 + 1

#print "first point long axis_ed =",first_point_long_axis_ed,'\n'
#print "second point long axis_ed =",second_point_long_axis_ed,'\n'
#print "distance long axis_ed =", distance_max_long_axis_ed
########################################################################
#In this section the es longitunial strain is calculaed
distance_max_long_axis_es = 0.0
first_point_long_axis_es = 0
second_point_long_axis_es = 0

counter6 = 0
for node7 in node_data_Annulus_center_es.values:
    node_label_7 = node_data_Annulus_center_es.values[counter6].nodeLabel
    node_coordinate_7 = node_data_Annulus_center_es.values[counter6].data
    counter6 = counter6 + 1

    counter7 = 0
    for node8 in node_data_endo_es.values:
        node_label_8 = node_data_endo_es.values[counter7].nodeLabel
        node_coordinate_8 = node_data_endo_es.values[counter7].data
        if (node_label_8 == second_point_long_axis_ed):
            if (node_label_7 != node_label_8):
                distance_long_axis_es = math.sqrt((node_coordinate_7[0] - node_coordinate_8[0])**2 + (node_coordinate_7[1]-node_coordinate_8[1])**2 + (node_coordinate_7[2]-node_coordinate_8[2])**2)
                distance_max_long_axis_es = distance_long_axis_es
                first_point_long_axis_es = node_label_7
                second_point_long_axis_es = node_label_8
        counter7 = counter7 + 1

#print "first point long axis_es =",first_point_long_axis_es,'\n'
#print "second point long axis_es =",second_point_long_axis_es,'\n'
#print "distance long axis_es =", distance_max_long_axis_es

longitudinal_strain = 100*(distance_max_long_axis_es - distance_max_long_axis_ed)/distance_max_long_axis_ed
print "longitudinal_strain=",longitudinal_strain
