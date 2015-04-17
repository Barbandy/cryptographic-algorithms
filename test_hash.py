#coding: UTF-8
import hashlib, pytest, subprocess, os
from hypothesis import given
import md5, ripemd160, sha1, gost94

def hash_md5(data):
    h = hashlib.md5()
    h.update(data)
    return  h.hexdigest()

	
def hash_sha1(data):
    h = hashlib.sha1()
    h.update(data)
    return  h.hexdigest()


def hash_ripemd160(data):
    h = hashlib.new('ripemd160')
    h.update(data)
    return  h.hexdigest()	


@given(str)
def test_md5(data):
    assert hash_md5(data) == md5.calc_md5(data)	


@given(str)	
def test_ripemd160(data):
    assert hash_ripemd160(data) == ripemd160.calc_ripemd160(data)
	

@given(str)	
def test_sha1(data):
    assert hash_sha1(data) == sha1.calc_sha1(data)
	

@given(str)		
def test_gost94(data):
    cmd_line= ['openssl', 'dgst', '-hex', '-md_gost94']
    pr = subprocess.Popen(cmd_line,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    res, err = pr.communicate(input=data)
    res = res[9:-1]
    assert  res == gost94.calc_gost94(data)
