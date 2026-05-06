PROJET USV MARITIME - COMMANDES DE LANCEMENT

Terminal 1 : lancer la simulation Gazebo

cd ~/gazebo_maritime_ws
colcon build --merge-install

export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:~/gazebo_maritime_ws/install/share/gazebo_maritime/models
export GZ_SIM_SYSTEM_PLUGIN_PATH=$GZ_SIM_SYSTEM_PLUGIN_PATH:~/gazebo_maritime_ws/install/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/gazebo_maritime_ws/install/lib

gz sim -r src/gazebo_maritime/worlds/sydney_regatta.sdf


Terminal 2 : lancer le script de navigation du bateau

python3 ~/gazebo_maritime_ws/src/gazebo_maritime/scripts/nav_direct.py
