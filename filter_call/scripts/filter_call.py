#!/usr/bin/env python

import rospy
import lesson_perception.srv
from sensor_msgs.msg import PointCloud2#!/usr/bin/env python

if __name__ == '__main__':
    rospy.init_node('filter_cloud', anonymous=True)
    rospy.wait_for_service('filter_cloud')
    try:
        # =======================
        # VOXEL GRID FILTER
        # =======================

        srvp = rospy.ServiceProxy('filter_cloud', lesson_perception.srv.FilterCloud)
        req = lesson_perception.srv.FilterCloudRequest()
        req.pcdfilename = rospy.get_param('~pcdfilename', '')
        req.operation = lesson_perception.srv.FilterCloudRequest.VOXELGRID
        # FROM THE SERVICE, ASSIGN POINTS
        req.input_cloud = PointCloud2()

        # ERROR HANDLING
        if req.pcdfilename == '':
            raise Exception('No file parameter found')

        # PACKAGE THE FILTERED POINTCLOUD2 TO BE PUBLISHED
        res_voxel = srvp(req)
        print('response received')
        if not res_voxel.success:
            raise Exception('Unsuccessful voxel grid filter operation')

        # PUBLISH VOXEL FILTERED POINTCLOUD2
        pub = rospy.Publisher('/perception_voxelGrid', PointCloud2, queue_size=1, latch=True)
        pub.publish(res_voxel.output_cloud)
        print("published: voxel grid filter response")
        rospy.spin()
    except Exception as e:
        print("Service call failed: %s" % str(e))