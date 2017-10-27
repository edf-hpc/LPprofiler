# -*- coding: utf-8 -*-
##############################################################################
#  This file is part of the LPprofiler profiling tool.                       #
#        Copyright (C) 2017  EDF SA                                          #
#                                                                            #
#  LPprofiler is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by      #
#  the Free Software Foundation, either version 3 of the License, or         #
#  (at your option) any later version.                                       #
#                                                                            #
#  LPprofiler is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#  GNU General Public License for more details.                              #
#                                                                            #
#  You should have received a copy of the GNU General Public License         #
#  along with LPprofiler.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                            #
##############################################################################

from collections import defaultdict

class MetricsManager:

    def __init__(self):
        self.metrics_count=defaultdict(lambda : defaultdict(lambda : defaultdict(float)))
        self.metrics_min={}
        self.metrics_max={}
        self.metrics_avg={}
        
    def add_metric(self,rank,metric_type,metric_name,count=1):

        self.metrics_count[metric_type][metric_name][rank]+=count

    def remove_metric(self,metric_type,metric_name):
            
        del self.metrics_count[metric_type][metric_name]

        
    def _metric_exists(self,metric_type,metric_name,rank=-1):
        if not metric_type in self.metrics_count:
            return False
        if not metric_name in self.metrics_count[metric_type]:
            return False
        if rank>=0 and not rank in self.metrics_count[metric_type][metric_name]:
            return False
        
        return True

    def get_metric_types(self):
        return list(self.metrics_count.keys())
    
    def get_metric_names(self,metric_type):
        if not metric_type in self.metrics_count:
            return []
        else:
            return list(self.metrics_count[metric_type].keys())

    def get_metric_count(self,metric_type,metric_name,rank):

        if not self._metric_exists(metric_type,metric_name,rank):
            return 0
        return self.metrics_count[metric_type][metric_name][rank]

    
    def get_metric_avg(self,metric_type,metric_name):

        # If already computed return the existent value
        if metric_type in self.metrics_avg and metric_name in self.metrics_avg[metric_type]:
            return self.metrics_avg[metric_type][metric_name]
        elif not self._metric_exists(metric_type,metric_name):
            return 0
        if not metric_type in self.metrics_avg:
            self.metrics_avg[metric_type]={}

        avg=0
        nbrank=0
        for rank,count in self.metrics_count[metric_type][metric_name].items():
            avg+=count
            nbrank+=1

        if nbrank!=0:
            self.metrics_avg[metric_type][metric_name]=avg/nbrank
        else:
            self.metrics_avg[metric_type][metric_name]=None
            
        return self.metrics_avg[metric_type][metric_name]
        
    def get_metric_min(self,metric_type,metric_name):

        # If already computed return the existent value
        if metric_type in self.metrics_min and metric_name in self.metrics_min[metric_type]:
            return self.metrics_min[metric_type][metric_name]
        elif not self._metric_exists(metric_type,metric_name):
            return None
        if not metric_type in self.metrics_min:
            self.metrics_min[metric_type]={}

        
        min_count=float("inf")
        min_rank=0
        for rank,count in self.metrics_count[metric_type][metric_name].items():
            if count < min_count:
                min_count=count
                min_rank=rank
                
        self.metrics_min[metric_type][metric_name]=(min_count,min_rank)
        
        return self.metrics_min[metric_type][metric_name]
        
    def get_metric_max(self,metric_type,metric_name):

        # If already computed return the existent value
        if metric_type in self.metrics_max and metric_name in self.metrics_max[metric_type]:
            return self.metrics_max[metric_type][metric_name]
        elif not self._metric_exists(metric_type,metric_name):
            return None
        if not metric_type in self.metrics_max:
            self.metrics_max[metric_type]={}

        
        
        max_count=-float("inf")
        max_rank=0
        for rank,count in self.metrics_count[metric_type][metric_name].items():
            if count > max_count:
                max_count=count
                max_rank=rank
                
        self.metrics_max[metric_type][metric_name]=(max_count,max_rank)
        return self.metrics_max[metric_type][metric_name]
        