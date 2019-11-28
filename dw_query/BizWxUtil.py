# -*- coding: utf-8 -*-
from django.http import HttpResponse
from .WXBizMsgCrypt import WXBizMsgCrypt, ResponseMessage, generateNonce
from xml.etree.cElementTree import fromstring


def getCryptor():
    # TODO hard code configuration
    sToken = "9AcDz9eC4vH1Ygt7sC6jjUvNP"
    sEncodingAESKey = "hGTY0NgybjLfGRNlQXhgB7jDNuQbPkoSH68SFdIR1Pa"
    sCorpID = "wwa6b01f2f06d58c58"
    return WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)


def responseEcho(request):
    sVerifyMsgSig = request.GET.get('msg_signature')
    sVerifyNonce = request.GET.get('nonce')
    sVerifyTimeStamp = request.GET.get('timestamp')
    sVerifyEchoStr = request.GET.get('echostr')

    wxcpt = getCryptor()

    ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce,
                                    sVerifyEchoStr)
    if ret != 0:
        print("ERR: VerifyURL ret: " + str(ret))
        return HttpResponse("ERR: VerifyURL ret: " + str(ret))

    return HttpResponse(sEchoStr)


# decrypt message and ruturn as python dict
def parseMessage(request):
    encrypted_xml = request.body.decode('utf-8')
    sVerifyMsgSig = request.GET.get('msg_signature')
    sVerifyNonce = request.GET.get('nonce')
    sVerifyTimeStamp = request.GET.get('timestamp')

    wxcpt = getCryptor()
    ret, xml_content = wxcpt.DecryptMsg(encrypted_xml, sVerifyMsgSig, sVerifyTimeStamp,
                                        sVerifyNonce)
    if ret != 0:
        print("ERR: VerifyURL ret: " + str(ret))
        return HttpResponse("ERR: VerifyURL ret: " + str(ret))

    type_fields = {
        "text": ["ToUserName", "FromUserName", "CreateTime", "MsgType", "Content",
                 "MsgId", "AgentID"],
        "image": ["ToUserName", "FromUserName", "CreateTime", "MsgType", "PicUrl",
                  "MediaId", "MsgId", "AgentID"],
        "voice": ["ToUserName", "FromUserName", "CreateTime", "MsgType", "Format",
                  "MediaId", "MsgId", "AgentID"],
        "video": ["ToUserName", "FromUserName", "CreateTime", "MsgType", "ThumbMediaId",
                  "MediaId", "MsgId", "AgentID"],
        "location": ["ToUserName", "FromUserName", "CreateTime", "MsgType", "Location_X",
                     "Location_Y", "Scale", "Label", "MsgId", "AgentID"],
        "link": ["ToUserName", "FromUserName", "CreateTime", "MsgType", "Title",
                 "Description", "PicUrl", "MsgId", "AgentID"],
        "event": ["ToUserName", "FromUserName", "CreateTime", "MsgType", "Event",
                  "EventKey", "AgentID"]
    }
    xml_tree = fromstring(xml_content)
    type_name = xml_tree.find("MsgType").text
    msg = {}
    for nodename in type_fields[type_name]:
        msg[nodename] = xml_tree.find(nodename).text
    return msg


def parseResponse(resp_dict):
    wxcpt = getCryptor()
    xml_message = ResponseMessage(resp_dict).xml
    nonce = generateNonce()
    ret, returnMsg = wxcpt.EncryptMsg(xml_message, nonce)
    if ret != 0:
        print("ERR: VerifyURL ret: " + str(ret))
        return HttpResponse("ERR: VerifyURL ret: " + str(ret))
    return HttpResponse(returnMsg)
