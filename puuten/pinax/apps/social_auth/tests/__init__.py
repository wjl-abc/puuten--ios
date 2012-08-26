#coding=utf-8
'''
from pinax.apps.social_auth.utils import setting


if setting('SOCIAL_AUTH_TEST_TWITTER', True):
    from social_auth.tests.twitter import *

if setting('SOCIAL_AUTH_TEST_FACEBOOK', True):
    from social_auth.tests.facebook import *

if setting('SOCIAL_AUTH_TEST_GOOGLE', True):
    from social_auth.tests.google import *
'''
import re

def check_WeiBo_Status(text):
    if re.search(r'(\d+)(?:日|元|号)',text) or re.search(r'(\d+)\.(\d+)',text) \
         or re.search(r'(\d+)\/(\d+)',text) \
         or re.search(r'(?:明天|今天|后天|今晚|明晚|优惠|折扣|促销|打折)',text) \
         or re.search(r'(?:周|星期|礼拜)(?:一|二|三|四|五|六|日|天)',text) :
        return True

#print check_WeiBo_Status("#大歌星[哨子]大八卦# 杨千嬅 于6月5日诞下儿子Torres[笑哈哈]，虽然连日来忙于照顾儿子，但她与老公丁子高有子万事足。12日杨千嬅在微博分享Torres的可爱新照片，她预计两、三个月左右复工。老公丁子高形容Torres是他人生最大的礼物[礼物]，很有成功感，并表示想生女儿，凑成一个“好”字[欢欢][乐乐]")
    
def facetext_to_facepic(text):
    face_list = '<ul class="faces_list faces_list_hot clearfix" node-type="hotFace" style=""><li action-type="insert" action-data="text=[伦敦奥火]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/5a/lundunaohuo_thumb.gif" alt="伦敦奥火" title="伦敦奥火"></li><li action-type="insert" action-data="text=[cai开心]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/e2/caikaixin_thumb.gif" alt="cai开心" title="cai开心"></li><li action-type="insert" action-data="text=[cai晃头]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/22/caihuangtou_thumb.gif" alt="cai晃头" title="cai晃头"></li><li action-type="insert" action-data="text=[不好意思]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/b4/lxhbuhaoyisi_thumb.gif" alt="不好意思" title="不好意思"></li><li action-type="insert" action-data="text=[加油啊]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/03/lxhjiayou_thumb.gif" alt="加油啊" title="加油啊"></li><li action-type="insert" action-data="text=[亲一口]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/88/lxhqinyikou_thumb.gif" alt="亲一口" title="亲一口"></li><li action-type="insert" action-data="text=[笑哈哈]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/32/lxhwahaha_thumb.gif" alt="笑哈哈" title="笑哈哈"></li><li action-type="insert" action-data="text=[din推撞]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/dd/dintuizhuang_thumb.gif" alt="din推撞" title="din推撞"></li><li action-type="insert" action-data="text=[lb味]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d1/lbwei_thumb.gif" alt="lb味" title="lb味"></li><li action-type="insert" action-data="text=[bobo纠结]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/f0/bobojiujie_thumb.gif" alt="bobo纠结" title="bobo纠结"></li><li action-type="insert" action-data="text=[g头晕]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/cf/guibao30touyun_thumb.gif" alt="g头晕" title="g头晕"></li><li action-type="insert" action-data="text=[bed凌乱]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/fa/brdlingluan_thumb.gif" alt="bed凌乱" title="bed凌乱"></li><li action-type="insert" action-data="text=[织]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/41/zz2_thumb.gif" alt="织" title="织"></li><li action-type="insert" action-data="text=[神马]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/60/horse2_thumb.gif" alt="神马" title="神马"></li><li action-type="insert" action-data="text=[浮云]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/bc/fuyun_thumb.gif" alt="浮云" title="浮云"></li><li action-type="insert" action-data="text=[给力]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/c9/geili_thumb.gif" alt="给力" title="给力"></li><li action-type="insert" action-data="text=[围观]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/f2/wg_thumb.gif" alt="围观" title="围观"></li><li action-type="insert" action-data="text=[威武]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/70/vw_thumb.gif" alt="威武" title="威武"></li><li action-type="insert" action-data="text=[熊猫]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6e/panda_thumb.gif" alt="熊猫" title="熊猫"></li><li action-type="insert" action-data="text=[兔子]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/81/rabbit_thumb.gif" alt="兔子" title="兔子"></li><li action-type="insert" action-data="text=[奥特曼]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/bc/otm_thumb.gif" alt="奥特曼" title="奥特曼"></li><li action-type="insert" action-data="text=[囧]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/15/j_thumb.gif" alt="囧" title="囧"></li><li action-type="insert" action-data="text=[互粉]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/89/hufen_thumb.gif" alt="互粉" title="互粉"></li><li action-type="insert" action-data="text=[礼物]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/c4/liwu_thumb.gif" alt="礼物" title="礼物"></li><li action-type="insert" action-data="text=[呵呵]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/ac/smilea_thumb.gif" alt="呵呵" title="呵呵"></li><li action-type="insert" action-data="text=[嘻嘻]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/0b/tootha_thumb.gif" alt="嘻嘻" title="嘻嘻"></li><li action-type="insert" action-data="text=[哈哈]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6a/laugh.gif" alt="哈哈" title="哈哈"></li><li action-type="insert" action-data="text=[可爱]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/14/tza_thumb.gif" alt="可爱" title="可爱"></li><li action-type="insert" action-data="text=[可怜]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/af/kl_thumb.gif" alt="可怜" title="可怜"></li><li action-type="insert" action-data="text=[挖鼻屎]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/a0/kbsa_thumb.gif" alt="挖鼻屎" title="挖鼻屎"></li><li action-type="insert" action-data="text=[吃惊]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/f4/cj_thumb.gif" alt="吃惊" title="吃惊"></li><li action-type="insert" action-data="text=[害羞]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6e/shamea_thumb.gif" alt="害羞" title="害羞"></li><li action-type="insert" action-data="text=[挤眼]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/c3/zy_thumb.gif" alt="挤眼" title="挤眼"></li><li action-type="insert" action-data="text=[闭嘴]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/29/bz_thumb.gif" alt="闭嘴" title="闭嘴"></li><li action-type="insert" action-data="text=[鄙视]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/71/bs2_thumb.gif" alt="鄙视" title="鄙视"></li><li action-type="insert" action-data="text=[爱你]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6d/lovea_thumb.gif" alt="爱你" title="爱你"></li><li action-type="insert" action-data="text=[泪]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/9d/sada_thumb.gif" alt="泪" title="泪"></li><li action-type="insert" action-data="text=[偷笑]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/19/heia_thumb.gif" alt="偷笑" title="偷笑"></li><li action-type="insert" action-data="text=[亲亲]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/8f/qq_thumb.gif" alt="亲亲" title="亲亲"></li><li action-type="insert" action-data="text=[生病]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/b6/sb_thumb.gif" alt="生病" title="生病"></li><li action-type="insert" action-data="text=[太开心]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/58/mb_thumb.gif" alt="太开心" title="太开心"></li><li action-type="insert" action-data="text=[懒得理你]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/17/ldln_thumb.gif" alt="懒得理你" title="懒得理你"></li><li action-type="insert" action-data="text=[右哼哼]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/98/yhh_thumb.gif" alt="右哼哼" title="右哼哼"></li><li action-type="insert" action-data="text=[左哼哼]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6d/zhh_thumb.gif" alt="左哼哼" title="左哼哼"></li><li action-type="insert" action-data="text=[嘘]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/a6/x_thumb.gif" alt="嘘" title="嘘"></li><li action-type="insert" action-data="text=[衰]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/af/cry.gif" alt="衰" title="衰"></li><li action-type="insert" action-data="text=[委屈]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/73/wq_thumb.gif" alt="委屈" title="委屈"></li><li action-type="insert" action-data="text=[吐]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/9e/t_thumb.gif" alt="吐" title="吐"></li><li action-type="insert" action-data="text=[打哈气]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/f3/k_thumb.gif" alt="打哈气" title="打哈气"></li><li action-type="insert" action-data="text=[抱抱]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/27/bba_thumb.gif" alt="抱抱" title="抱抱"></li><li action-type="insert" action-data="text=[怒]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/7c/angrya_thumb.gif" alt="怒" title="怒"></li><li action-type="insert" action-data="text=[疑问]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/5c/yw_thumb.gif" alt="疑问" title="疑问"></li><li action-type="insert" action-data="text=[馋嘴]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/a5/cza_thumb.gif" alt="馋嘴" title="馋嘴"></li><li action-type="insert" action-data="text=[拜拜]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/70/88_thumb.gif" alt="拜拜" title="拜拜"></li><li action-type="insert" action-data="text=[思考]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/e9/sk_thumb.gif" alt="思考" title="思考"></li><li action-type="insert" action-data="text=[汗]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/24/sweata_thumb.gif" alt="汗" title="汗"></li><li action-type="insert" action-data="text=[困]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/7f/sleepya_thumb.gif" alt="困" title="困"></li><li action-type="insert" action-data="text=[睡觉]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6b/sleepa_thumb.gif" alt="睡觉" title="睡觉"></li><li action-type="insert" action-data="text=[钱]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/90/money_thumb.gif" alt="钱" title="钱"></li><li action-type="insert" action-data="text=[失望]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/0c/sw_thumb.gif" alt="失望" title="失望"></li><li action-type="insert" action-data="text=[酷]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/40/cool_thumb.gif" alt="酷" title="酷"></li><li action-type="insert" action-data="text=[花心]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/8c/hsa_thumb.gif" alt="花心" title="花心"></li><li action-type="insert" action-data="text=[哼]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/49/hatea_thumb.gif" alt="哼" title="哼"></li><li action-type="insert" action-data="text=[鼓掌]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/36/gza_thumb.gif" alt="鼓掌" title="鼓掌"></li><li action-type="insert" action-data="text=[晕]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d9/dizzya_thumb.gif" alt="晕" title="晕"></li><li action-type="insert" action-data="text=[悲伤]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/1a/bs_thumb.gif" alt="悲伤" title="悲伤"></li><li action-type="insert" action-data="text=[抓狂]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/62/crazya_thumb.gif" alt="抓狂" title="抓狂"></li><li action-type="insert" action-data="text=[黑线]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/91/h_thumb.gif" alt="黑线" title="黑线"></li><li action-type="insert" action-data="text=[阴险]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6d/yx_thumb.gif" alt="阴险" title="阴险"></li><li action-type="insert" action-data="text=[怒骂]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/89/nm_thumb.gif" alt="怒骂" title="怒骂"></li><li action-type="insert" action-data="text=[心]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/40/hearta_thumb.gif" alt="心" title="心"></li><li action-type="insert" action-data="text=[伤心]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/ea/unheart.gif" alt="伤心" title="伤心"></li><li action-type="insert" action-data="text=[猪头]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/58/pig.gif" alt="猪头" title="猪头"></li><li action-type="insert" action-data="text=[ok]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d6/ok_thumb.gif" alt="ok" title="ok"></li><li action-type="insert" action-data="text=[耶]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d9/ye_thumb.gif" alt="耶" title="耶"></li><li action-type="insert" action-data="text=[good]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d8/good_thumb.gif" alt="good" title="good"></li><li action-type="insert" action-data="text=[不要]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/c7/no_thumb.gif" alt="不要" title="不要"></li><li action-type="insert" action-data="text=[赞]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d0/z2_thumb.gif" alt="赞" title="赞"></li><li action-type="insert" action-data="text=[来]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/40/come_thumb.gif" alt="来" title="来"></li><li action-type="insert" action-data="text=[弱]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d8/sad_thumb.gif" alt="弱" title="弱"></li><li action-type="insert" action-data="text=[蜡烛]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/91/lazu_thumb.gif" alt="蜡烛" title="蜡烛"></li><li action-type="insert" action-data="text=[蛋糕]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6a/cake.gif" alt="蛋糕" title="蛋糕"></li><li action-type="insert" action-data="text=[钟]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d3/clock_thumb.gif" alt="钟" title="钟"></li><li action-type="insert" action-data="text=[话筒]"><img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/1b/m_thumb.gif" alt="话筒" title="话筒"></li></ul>'
    textarray = re.findall("\[.+?\]", face_list)
    picarray={}
    for match in textarray:
        
        su = re.search(match+"(.*?)</li>",face_list).group()
        picarray[match] = re.search(match+"(.*?)</li>",face_list).group()
    face_list = {'[伦敦奥火]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/5a/lundunaohuo_thumb.gif" alt="伦敦奥火" title="伦敦奥火">',
        '[cai开心]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/e2/caikaixin_thumb.gif" alt="cai开心" title="cai开心">',
        '[cai晃头]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/22/caihuangtou_thumb.gif" alt="cai晃头" title="cai晃头">',
        '[不好意思]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/b4/lxhbuhaoyisi_thumb.gif" alt="不好意思" title="不好意思">',
        '[加油啊]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/03/lxhjiayou_thumb.gif" alt="加油啊" title="加油啊">',
        '[亲一口]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/88/lxhqinyikou_thumb.gif" alt="亲一口" title="亲一口">',
        '[笑哈哈]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/32/lxhwahaha_thumb.gif" alt="笑哈哈" title="笑哈哈">',
        '[din推撞]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/dd/dintuizhuang_thumb.gif" alt="din推撞" title="din推撞">',
        '[lb味]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d1/lbwei_thumb.gif" alt="lb味" title="lb味">',
        '[bobo纠结]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/f0/bobojiujie_thumb.gif" alt="bobo纠结" title="bobo纠结">',
        '[g头晕]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/cf/guibao30touyun_thumb.gif" alt="g头晕" title="g头晕">',
        '[bed凌乱]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/fa/brdlingluan_thumb.gif" alt="bed凌乱" title="bed凌乱">',
        '[织]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/41/zz2_thumb.gif" alt="织" title="织">',
        '[神马]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/60/horse2_thumb.gif" alt="神马" title="神马">',
        '[浮云]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/bc/fuyun_thumb.gif" alt="浮云" title="浮云">',
        '[给力]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/c9/geili_thumb.gif" alt="给力" title="给力">',
        '[围观]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/f2/wg_thumb.gif" alt="围观" title="围观">',
        '[威武]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/70/vw_thumb.gif" alt="威武" title="威武">',
        '[熊猫]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6e/panda_thumb.gif" alt="熊猫" title="熊猫">',
        '[兔子]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/81/rabbit_thumb.gif" alt="兔子" title="兔子">',
        '[奥特曼]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/bc/otm_thumb.gif" alt="奥特曼" title="奥特曼">',
        '[囧]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/15/j_thumb.gif" alt="囧" title="囧">',
        '[互粉]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/89/hufen_thumb.gif" alt="互粉" title="互粉">',
        '[礼物]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/c4/liwu_thumb.gif" alt="礼物" title="礼物">',
        '[呵呵]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/ac/smilea_thumb.gif" alt="呵呵" title="呵呵">',
        '[嘻嘻]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/0b/tootha_thumb.gif" alt="嘻嘻" title="嘻嘻">',
        '[哈哈]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6a/laugh.gif" alt="哈哈" title="哈哈">',
        '[可爱]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/14/tza_thumb.gif" alt="可爱" title="可爱">',
        '[可怜]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/af/kl_thumb.gif" alt="可怜" title="可怜">',
        '[挖鼻屎]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/a0/kbsa_thumb.gif" alt="挖鼻屎" title="挖鼻屎">',
        '[吃惊]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/f4/cj_thumb.gif" alt="吃惊" title="吃惊">',
        '[害羞]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6e/shamea_thumb.gif" alt="害羞" title="害羞">',
        '[挤眼]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/c3/zy_thumb.gif" alt="挤眼" title="挤眼">',
        '[闭嘴]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/29/bz_thumb.gif" alt="闭嘴" title="闭嘴">',
        '[鄙视]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/71/bs2_thumb.gif" alt="鄙视" title="鄙视">',
        '[爱你]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6d/lovea_thumb.gif" alt="爱你" title="爱你">',
        '[泪]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/9d/sada_thumb.gif" alt="泪" title="泪">',
        '[偷笑]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/19/heia_thumb.gif" alt="偷笑" title="偷笑">',
        '[亲亲]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/8f/qq_thumb.gif" alt="亲亲" title="亲亲">',
        '[生病]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/b6/sb_thumb.gif" alt="生病" title="生病">',
        '[太开心]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/58/mb_thumb.gif" alt="太开心" title="太开心">',
        '[懒得理你]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/17/ldln_thumb.gif" alt="懒得理你" title="懒得理你">',
        '[右哼哼]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/98/yhh_thumb.gif" alt="右哼哼" title="右哼哼">',
        '[左哼哼]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6d/zhh_thumb.gif" alt="左哼哼" title="左哼哼">',
        '[嘘]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/a6/x_thumb.gif" alt="嘘" title="嘘">',
        '[衰]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/af/cry.gif" alt="衰" title="衰">',
        '[委屈]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/73/wq_thumb.gif" alt="委屈" title="委屈">',
        '[吐]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/9e/t_thumb.gif" alt="吐" title="吐">',
        '[打哈气]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/f3/k_thumb.gif" alt="打哈气" title="打哈气">',
        '[抱抱]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/27/bba_thumb.gif" alt="抱抱" title="抱抱">',
        '[怒]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/7c/angrya_thumb.gif" alt="怒" title="怒">',
        '[疑问]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/5c/yw_thumb.gif" alt="疑问" title="疑问">',
        '[馋嘴]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/a5/cza_thumb.gif" alt="馋嘴" title="馋嘴">',
        '[拜拜]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/70/88_thumb.gif" alt="拜拜" title="拜拜">',
        '[思考]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/e9/sk_thumb.gif" alt="思考" title="思考">',
        '[汗]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/24/sweata_thumb.gif" alt="汗" title="汗">',
        '[困]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/7f/sleepya_thumb.gif" alt="困" title="困">',
        '[睡觉]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6b/sleepa_thumb.gif" alt="睡觉" title="睡觉">',
        '[钱]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/90/money_thumb.gif" alt="钱" title="钱">',
        '[失望]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/0c/sw_thumb.gif" alt="失望" title="失望">',
        '[酷]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/40/cool_thumb.gif" alt="酷" title="酷">',
        '[花心]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/8c/hsa_thumb.gif" alt="花心" title="花心">',
        '[哼]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/49/hatea_thumb.gif" alt="哼" title="哼">',
        '[鼓掌]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/36/gza_thumb.gif" alt="鼓掌" title="鼓掌">',
        '[晕]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d9/dizzya_thumb.gif" alt="晕" title="晕">',
        '[悲伤]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/1a/bs_thumb.gif" alt="悲伤" title="悲伤">',
        '[抓狂]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/62/crazya_thumb.gif" alt="抓狂" title="抓狂">',
        '[黑线]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/91/h_thumb.gif" alt="黑线" title="黑线">',
        '[阴险]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6d/yx_thumb.gif" alt="阴险" title="阴险">',
        '[怒骂]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/89/nm_thumb.gif" alt="怒骂" title="怒骂">',
        '[心]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/40/hearta_thumb.gif" alt="心" title="心">',
        '[伤心]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/ea/unheart.gif" alt="伤心" title="伤心">',
        '[猪头]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/58/pig.gif" alt="猪头" title="猪头">',
        '[ok]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d6/ok_thumb.gif" alt="ok" title="ok">',
        '[耶]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d9/ye_thumb.gif" alt="耶" title="耶">',
        '[good]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d8/good_thumb.gif" alt="good" title="good">',
        '[不要]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/c7/no_thumb.gif" alt="不要" title="不要">',
        '[赞]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d0/z2_thumb.gif" alt="赞" title="赞">',
        '[来]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/40/come_thumb.gif" alt="来" title="来">',
        '[弱]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d8/sad_thumb.gif" alt="弱" title="弱">',
        '[蜡烛]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/91/lazu_thumb.gif" alt="蜡烛" title="蜡烛">',
        '[蛋糕]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/6a/cake.gif" alt="蛋糕" title="蛋糕">',
        '[钟]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/d3/clock_thumb.gif" alt="钟" title="钟">',
        '[话筒]':'<img src="http://img.t.sinajs.cn/t35/style/images/common/face/ext/normal/1b/m_thumb.gif" alt="话筒" title="话筒">',
        }
    textarray = re.findall("\[.+?\]", text)
    for item in textarray:
        text = text.replace(str(item),face_list[str(item)])
    return text
#print facetext_to_facepic("fds[din推撞]afdsf[伦敦奥火]fds[din推撞]a[伦敦奥火]f")
import urllib2
from StringIO import StringIO
def shorturl_show(text):
    shorturl = re.search("http://t.cn/(.+)", text).group()
    request = urllib2.Request(shorturl)
    #request.add_header('Accept-encoding', 'gzip')
    sock=urllib2.urlopen(request) 
    print sock.info() 
    buf = StringIO( sock.read())
    source = buf.read()
    #source=source.decode('utf-8-sig')
    print source
    print sock.geturl()
#shorturl_show("拍了几张，这张也许还好。我在这里:#海淀区#@雕刻时光咖啡馆http://t.cn/GZzaV")
#print check_WeiBo_Status("我不是了，有3月打折事")
import logging
logger = None
if not logger:
    logger = logging.getLogger('SocialAuth')
    logger.setLevel(logging.DEBUG)


def log(level, *args, **kwargs):
    """Small wrapper around logger functions."""
    {'debug': logger.debug,
     'error': logger.error,
     'exception': logger.exception,
     'warn': logger.warn}[level](*args, **kwargs)
"""log('error', unicode("aaaaaa哈哈"), exc_info=True, extra={
                    'request': "exinfo"
                })
                
import Image
import urllib
import os
image = "http://ww1.sinaimg.cn/thumbnail/69c7be75jw1dv5xwp34cmj.jpg"
img = urllib.urlretrieve(image,image.split('/')[-1])
img = Image.open(image.split('/')[-1],"r")
width,height =  img.size
img.save(image.split('/')[-1],img.format)
os.remove(image.split('/')[-1])
"""
def check_WeiBo_Text_NotSaved(text):
    if re.search(r'#(?:晚安|语|相册|分享|推荐|歌星|健康|明星|微薄|问候|早安|时尚|中国|清晨|快递)#',text) :
        return True
    else:
        return False

print "Unexpected error: (<class 'psycopg2.DataError'>, DataError('\xe9\x8c\xaf\xe8\xaa\xa4:  \xe5\x80\xbc\xe5\xb0\x8d\xe5\x9e\x8b\xe5\x88\xa5 character varying(1) \xe8\x80\x8c\xe8\xa8\x80\xe5\xa4\xaa\xe9\x95\xb7\n',), <traceback object at 0x02209C88>)"