#PyDispatcher License

#    Copyright (c) 2001-2003, Patrick K. O'Brien and Contributors
#    All rights reserved.
#    
#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions
#    are met:
#    
#        Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#    
#        Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials
#        provided with the distribution.
#    
#        The name of Patrick K. O'Brien, or the name of any Contributor,
#        may not be used to endorse or promote products derived from this 
#        software without specific prior written permission.
#    
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#    COPYRIGHT HOLDERS AND CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
#    INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#    HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#    OF THE POSSIBILITY OF SUCH DAMAGE. 

# Changes to original test from PyDispatcher:
#   - Changed the import line
#   - Renamed test2 to sftest2 so wouldn't error out in the nose
#     testing suite

from aossi.saferef import *

import unittest
class Test1( object):
	def x( self ):
		pass
def sftest2(obj):
	pass
class Test2( object ):
	def __call__( self, obj ):
		pass
class Tester (unittest.TestCase):
	def setUp (self):
		ts = []
		ss = []
		for x in xrange( 5000 ):
			t = Test1()
			ts.append( t)
			s = safeRef(t.x, self._closure )
			ss.append( s)
		ts.append( sftest2 )
		ss.append( safeRef(sftest2, self._closure) )
		for x in xrange( 30 ):
			t = Test2()
			ts.append( t)
			s = safeRef(t, self._closure )
			ss.append( s)
		self.ts = ts
		self.ss = ss
		self.closureCount = 0
	def tearDown( self ):
		del self.ts
		del self.ss
	def testIn(self):
		"""Test the "in" operator for safe references (cmp)"""
		for t in self.ts[:50]:
			assert safeRef(t.x) in self.ss
	def testValid(self):
		"""Test that the references are valid (return instance methods)"""
		for s in self.ss:
			assert s()
	def testShortCircuit (self):
		"""Test that creation short-circuits to reuse existing references"""
		sd = {}
		for s in self.ss:
			sd[s] = 1
		for t in self.ts:
			if hasattr( t, 'x'):
				assert sd.has_key( safeRef(t.x))
			else:
				assert sd.has_key( safeRef(t))
	def testRepresentation (self):
		"""Test that the reference object's representation works

		XXX Doesn't currently check the results, just that no error
			is raised
		"""
		repr( self.ss[-1] )
		
	def test(self):
		self.closureCount = 0
		wholeI = len(self.ts)
		for i in xrange( len(self.ts)-1, -1, -1):
			del self.ts[i]
			if wholeI-i != self.closureCount:
				"""Unexpected number of items closed, expected %s, got %s closed"""%( wholeI-i,self.closureCount)
		
	def _closure(self, ref):
		"""Dumb utility mechanism to increment deletion counter"""
		self.closureCount +=1

def getSuite():
	return unittest.makeSuite(Tester,'test')

if __name__ == "__main__":
	unittest.main ()
