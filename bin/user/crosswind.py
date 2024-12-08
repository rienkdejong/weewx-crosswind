#    SPDX-License-Identifier: GPL-2.0
#    Copyright (c) 2024 Rienk de Jong <rienk@rienkdejong.nl>
#
#    See the file LICENSE for your full rights.
#
"""This extension adds crosswind and head/tail-wind component

REQUIRES WeeWX V5.0 OR LATER

"""
import math

import weewx
import weewx.units
import weewx.xtypes
from weewx.engine import StdService
from weewx.units import ValueTuple


class CrossWind(weewx.xtypes.XType):

    def __init__(self, runway):
        # Save the algorithm to be used.
        self.runway = runway

    def get_scalar(self, obs_type, record, db_manager):
        # We only know how to calculate 'vapor_p'. For everything else, raise an exception UnknownType
        if obs_type != 'cross_wind' and obs_type != 'head_wind':
            raise weewx.UnknownType(obs_type)

        # We need outTemp in order to do the calculation.
        if 'windDir' not in record or record['windDir'] is None:
            raise weewx.CannotCalculate(obs_type)
        unit_and_group = weewx.units.getStandardUnitType(record['usUnits'], 'windSpeed')
#        unit_and_group = weewx.units.getStandardUnitType(record['metricUnits'], 'windSpeed')

        windSpeed_vt = ValueTuple(record['windSpeed'], *unit_and_group)
        windSpeed_ms_vt = weewx.units.convert(windSpeed_vt, 'meter_per_second')

        windDir=record['windDir']
        #windSpeed=windSpeed_ms_vt[0]
        windSpeed=record['windSpeed']

        runway=50

        windAngle=runway-windDir

        v_cross_wind=abs(windSpeed*math.sin(windAngle*(math.pi/180)))
        #v_cross_wind=windSpeed
        #v_cross_wind=math.sin(windAngle*(math.pi/180))
        #v_cross_wind=windAngle
        v_head_wind=abs(windSpeed*math.cos(windAngle*(math.pi/180)))
        #v_head_wind=windSpeed
        #v_head_wind=math.cos(windAngle*(math.pi/180))
        
        
        cross_wind=ValueTuple(v_cross_wind, 'meter_per_second', 'group_speed')
        head_wind=ValueTuple(v_head_wind, 'meter_per_second', 'group_speed')

        if obs_type == 'cross_wind':
            return cross_wind
        else:
            return head_wind


class CrossWindService(StdService):
    """ WeeWX service whose job is to register the XTypes extension VaporPressure with the
    XType system.
    """

    def __init__(self, engine, config_dict):
        super(CrossWindService, self).__init__(engine, config_dict)

        # Get the desired algorithm. Default to "simple".
        try:
            runway = config_dict['CrossWind']['runway']
        except KeyError:
            runway = 53

        # Instantiate an instance of VaporPressure:
        self.cw = CrossWind(runway)
        # Register it:
        weewx.xtypes.xtypes.append(self.cw)

    def shutDown(self):
        # Remove the registered instance:
        weewx.xtypes.xtypes.remove(self.cw)


# Tell the unit system what group our new observation type, 'vapor_p', belongs to:
weewx.units.obs_group_dict['cross_wind'] = "group_speed"
weewx.units.obs_group_dict['head_wind'] = "group_speed"
