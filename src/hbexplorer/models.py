#/**
# * Copyright 2007 The Apache Software Foundation
# *
# * Licensed to the Apache Software Foundation (ASF) under one
# * or more contributor license agreements.  See the NOTICE file
# * distributed with this work for additional information
# * regarding copyright ownership.  The ASF licenses this file
# * to you under the Apache License, Version 2.0 (the
# * "License"); you may not use this file except in compliance
# * with the License.  You may obtain a copy of the License at
# *
# *     http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# */

from django.db import models
from django.contrib.auth.models import User
from urllib2 import urlopen, Request, HTTPError, URLError
import json

class ClusterAddress(models.Model):
    """
    Holds metadata about all the known clusters.
    """
    owner = models.ForeignKey(User, db_index=True)
    address = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1024)

    class Meta:
        ordering = ["address"]

class ClusterInfo(object):
    
    def __init__(self, clusterid):
        self.clusterid = clusterid
        
    def getTables(self):
        url = "http://" + self.clusterid + "/"
        request = Request(url, headers={"Accept":"application/json"})
        try:
            data = urlopen(request, timeout=30).read()
        except HTTPError, e:
            print "HTTP error: %d" % e.code
        except URLError, e:
            print "Network error: %s" % e.reason.args[1]
        json_data = json.loads(data)
        return [ table["name"] for table in json_data["table"] ]
        
        