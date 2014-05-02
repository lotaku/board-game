#!/usr/bin/env python
# encoding: utf-8
class CEntity:

    def __init__(self):
        self.m_Id=0
        self.m_Name='UNDEFINED'

    def CompName(self):
        return self.m_Name.lower()

entity = CEntity()
