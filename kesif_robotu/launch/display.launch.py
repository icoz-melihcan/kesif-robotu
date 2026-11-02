import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # Paketin kurulduğu yeri bul (install/kesif_robotu/share/kesif_robotu)
    paket_yolu = get_package_share_directory('kesif_robotu')
    xacro_dosyasi = os.path.join(paket_yolu, 'urdf', 'kesif_robotu.urdf.xacro')

    # xacro komutunu çalıştırıp düz URDF metnini elde et
    robot_description = ParameterValue(
        Command(['xacro ', xacro_dosyasi]), value_type=str
    )

    # 1) URDF'yi okur, parçaların birbirine göre konumlarını (TF) yayınlar
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
    )

    # 2) Hareketli eklemler için kaydırma çubukları açar
    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
    )

    # 3) Görselleştirme aracı
    rviz = Node(package='rviz2', executable='rviz2')

    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz,
    ])