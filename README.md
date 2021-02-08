# Universal Devices BASpi-Edge 6UI/6R NodeServer

## Based on the Contemporary Controls BASpi-Edge Controller

![BASpi-Edge DashBoard](https://github.com/sjpbailey/udi-poly-baspi-edge-master/blob/2abda35479e413148706de1e4f42e2e0e8893785/Images/BASpiEdgedashboards.jpg)

![BASpi-Edge Controller](https://github.com/sjpbailey/udi-poly-baspi-edge-master/blob/master/Images%2Fbasedge.jpg)

## BASpi-Egge DIY BacNet Control Device by Contemporary Controls

* Main
[Contemporary Controls BASpi Edge](https://www.ccontrols.com/basautomation/baspiedge.php)
* BASpi 6U6R Controller
[Contemporary Controls BASpi 6U6R](https://www.ccontrols.com/pdf/ds/BASPI-datasheet.pdf)
* BASpi 6U6R Installation
[Contemporary Controls BASpi 6U6R Install](https://www.ccontrols.com/pdf/BASpi-hardware-install-guide.pdf)
* BASpi 6U4R2A Controller
[Contemporary Controls BASpi 6U4R2A](https://www.ccontrols.com/pdf/ds/BASPI-AO2-datasheet.pdf)
* BASpi 6U4R2A Installation
[Contemporary Controls BASpi 6U4R2A Install](https://www.ccontrols.com/pdf/TD180600.pdf)
* BASpi Controller Configuration
[Contemporary Controls BASpi Configuration](https://www.ccontrols.com/pdf/is/BASPI-QSGuide.pdf)
* BASpi Controller Configuration
[Contemporary Controls BASpi-Edge Configuration](https://www.ccontrols.com/pdf/install/BASpi-Edge66_TD181400.pdf)

### Why

* The purpose of this Nodeserver is for custom control for general Home automation for up to six 6, Binary Outputs and six 6 Universal Inputs. This Poly can be used to control devices as is, also to expose progamming for custom control routines for all home automation.

* It utilizing the Contemporary Controls BASpi Edge control Module.
Please see links above for information & configuration of this Device.

* This will be included in a Network series for custom home control for Irrigation, Pool, six 6 car garage door controller, HVAC, VVT, Boiler, Well along with any custom control you create utilizing the bascontrolns module https://github.com/sjpbailey/bascontrol_ns.

#### Future

* This is for the BASpi-Edge 6U/6R module theis will include the BASpi-Edge 6U4R2A in the future.
Would like to add pulldowns for the Universal Inputs on this someday for editing within the ISY.
On the CC GUI the universal inputs have a large list of configurable UOM's of their own for this node server they are all raw values with no displayed type in the ISY.
Please see configuration quick start link above. On page two, it shows the GUI for the device. On their GUI you can pick on each universal input to configure its type and seperate UOM's unit of measure(s). Also see the viedo below.

![Future Adds](https://github.com/sjpbailey/udi-poly-baspi-edge-master/blob/63a4bd81e3fbe92ca35769a14ea383638b190d20/Images%2Fshot_3.png)

[Universal Input Configuration Viedo](https://www.youtube.com/watch?v=hTd1mR7npP4)

* Python 3.7.7

* Supported Nodes
  * Six 6 Universal Inputs
  * Six 6 Binary Outputs
  
##### Configuration

###### Defaults

* Default Short Poll:  Every 60 seconds
* Default Long Poll: Every 4 minutes (heartbeat)
* requirments [bascontrol_ns](https://pypi.org/project/bascontrolns/) module pip install bascontrolns

###### User Provided

* Enter your IP address for your BASpi-Edge controller,
* key = baspiedge1_ip
* Value = Enter Your BASpi Edge IP Address.
* Save and restart the NodeServer
* sjb
