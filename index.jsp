<body style="overflow: hidden;" class="mainPageBg" topmargin="0" leftmargin="0" scroll="no" onclick="doContinueWork();" onload="loadRelationItem('defaultpage');toggleLanguageForDoc(document);" languageStatus="<c:out value='${sessionScope.gui_languageStatus}'/>" ondragstart="window.event.returnValue=false;" oncontextmenu="window.event.returnValue=false;" onselectstart="event.returnValue=false;">
<input type="hidden" name="area" value="<c:out value='${area}'/>" />
<input type="hidden" name="message" value="<c:out value='${margueeMsg}'/>"  />
<iframe id="exportToExcelFrame" src=""  style="display:none;" ></iframe>
<iframe id="session" src="session.jsp"  style="display:none;" ></iframe>
<iframe id="logout" src="logout.jsp"  style="display:none;" ></iframe>
<iframe id="exportRunCardFrame" src=""  style="display:none;" ></iframe>


<%-- Title --------------------------------------------------------------------%>
<table border="0" cellpadding="0" cellspacing="0" style="table-layout:fixed; position:absolute; top:0px; left:0px; border-collapse: collapse;" bordercolor="#111111" width="100%" height="100%">
  <tr id="titleTR" >
    <td width="100%" height="35">
	<div id="titleBar" style="height:35px; width:100%; Z-INDEX:12;">
	<table border="0" cellspacing="0" style="TABLE-LAYOUT: fixed; BORDER-COLLAPSE: collapse" bordercolor="#111111" width="100%" cellpadding="0">
		<tr>
		<td width="17" height="35"><img border="0" src="<c:out value='${sessionScope.gui_skinPath}'/>/bleft.gif"></td>
		<td width="100%" height="35" background="<c:out value='${sessionScope.gui_skinPath}'/>/bg.jpg" align="center" valign="middle">
			<table border="0" cellspacing="0" style="TABLE-LAYOUT: fixed; BORDER-COLLAPSE: collapse"
 ordercolor="#111111" width="99%" cellpadding="0">
				<tr style="font-size:10pt;">
					<td width="85" height="26">
						<span><img src="<c:out value='${sessionScope.gui_skinPath}'/>/Cynosure_Logo2.gif" width="82" height="26"></span>
					</td>				
					<td width="20%" height="26" >
						<span style="font-family:Arial Black; color:#585894">-</span>
						<span><img src="<c:out value='${sessionScope.gui_skinPath}'/>/VisEra_Logo2.gif" width="38" height="26"></span>
						<span style="font-family:Arial Black; color:#585894; font-size:12pt;"><%=titleName %></span>
					</td>
					
				
					 <td width="50%" height="26" align="center"  valign="middle">
					 	<span id="functionName" class="functionName">OMI</span>
					 </td>
					 <td width="15%"  align=left height="26" valign="left">
					 	<span id="currentLayout" class="currentLocation" ><%= GuiUtility.getParameter(session,"global_layoutId","")%></span>
					</td>
					 <td width="15%"  align="right" height="26" valign="right">
					 	<span id="currentLocation" class="currentLocation"><%= GlobalValueUtil.getLocation(session,"")%></span>
					 	<!-- 拿掉超連結 -->
					 	<!-- <span id="currentLocation" class="currentLocation" onclick="jumpToLocationInfo(this.innerText)" style="cursor:hand"><%= GlobalValueUtil.getLocation(session,"")%></span> -->
						<span onclick="window.close()" class="iconBtnType2" onmouseover="this.className='iconBtnType1'" onmouseout="this.className='iconBtnType2'"><input type="image" hidefocus src="<c:out value='${sessionScope.gui_skinPath}'/>/close.gif" width="23" height="23" title="Exit"></span>
					</td>
					<td width="0%" align="right" height="26"  valign="middle">
						
						
						<!-- <span onclick="doBackHome();" class="iconBtnType2" onmouseover="this.className='iconBtnType1'" onmouseout="this.className='iconBtnType2'"><input type="image" hidefocus src="<c:out value='${sessionScope.gui_skinPath}'/>/Home.gif" width="23" height="23" title="Home"></span> -->
						<!-- <span onclick="doRefresh();" class="iconBtnType2" onmouseover="this.className='iconBtnType1'" onmouseout="this.className='iconBtnType2'"><input type="image" hidefocus src="<c:out value='${sessionScope.gui_skinPath}'/>/refresh.gif" width="23" height="23" title="Refresh"></span> -->
						<!-- <span onclick="doScreenChange();" class="iconBtnType2" onmouseover="this.className='iconBtnType1'" onmouseout="this.className='iconBtnType2'"><input type="image" hidefocus src="<c:out value='${sessionScope.gui_skinPath}'/>/FullScreenIcon.gif" width="20" height="23" title="Screen Change"></span>  -->
						<!-- <span onclick="window.close()" class="iconBtnType2" onmouseover="this.className='iconBtnType1'" onmouseout="this.className='iconBtnType2'"><input type="image" hidefocus src="<c:out value='${sessionScope.gui_skinPath}'/>/close.gif" width="23" height="23" title="Exit"></span> -->
 	  				<td>
				</tr>
			</table>
		</td>
		<td width="22" height="35"><img border="0" src="<c:out value='${sessionScope.gui_skinPath}'/>/bright.gif"></td>
		</tr>
	</table>
	</div>   
    </td>
  </tr>
 
  <tr>
    <td height="100%" width="100%">
    <table border="0" cellpadding="0" cellspacing="0" style="table-layout:fixed; border-collapse: collapse" bordercolor="#111111" height="100%" width="100%">
      <tr>
      
        <td width="100%">
        <%--Work Area------------------------------------------------------------------%>
<div id="mainWorkArea" class="mainWorkArea">
<table border="0" cellspacing="0" width="100%" height="100%" style="table-layout:fixed;" cellpadding="0" bordercolorlight="#808080" bordercolordark="#FFFFFF">
  <tr>
    <td width="100%" height="4" background="<c:out value='${sessionScope.gui_skinPath}'/>/obj_head_03.gif"></td>
  </tr>
  <input id="functionId" type="hidden" name="" value="">
  <input id="functionUrl" type="hidden" name="" value="">
  <tr>
    <td width="100%" height="105%">
		<iframe onfocus="moveMenu('left'); doContinueWork();" width="100%" height="100%" scrolling="no" marginwidth="0" marginheight="0" frameborder="0" name="mainWorkAreaFrame" id="workAreaFrame" src="MainGui.jsp"></iframe>
    </td>
  </tr>
</table>

</div>
        </td>
      </tr>
    </table>
    </td>
  </tr>
  <tr>
    <td width="100%" height="3" background="<c:out value='${sessionScope.gui_skinPath}'/>/obj_foot2.gif"></td>
  </tr>
  <tr>

    <td width="100%" height="40" bgcolor="#FFFFFF">

<link rel="StyleSheet" href="<c:out value='${sessionScope.gui_skinPath}'/>/statusBar.css" type="text/css"/>
<script src="<c:out value='${sessionScope.gui_jsPath}'/>/statusBar.js" type="text/javascript"></script>
<div id="statusBar" style="BORDER:#5a108b 0px solid; Z-INDEX:1; LEFT:2px; WIDTH:100%; HEIGHT:38px">
	<table border="0" cellspacing="0" width="100%" height="32" style="table-layout:fixed;" cellpadding="0" align="center">
		<tr>
			<td width="10" height="32"><image src="<c:out value='${sessionScope.gui_skinPath}'/>/bbs_left.gif" width="10" height="32"></image></td>
			<td width="300" background="<c:out value='${sessionScope.gui_skinPath}'/>/bbs_bg.gif" height="32">
				<span class="statusBar_ItemType1" id="currentUserId" onclick=""><%= GlobalValueUtil.getUserId(session,"")%></span>				
			</td>
			<td width="100%" background="<c:out value='${sessionScope.gui_skinPath}'/>/bbs_bg.gif" height="32">
				<span class="statusBar_ItemType1" id="statusBar2" onclick=""><marquee direction=left scrollamount='2' scrolldelay='150'  ><%=margueeMsg%></span>					
			</td>
			<!-- 
			<td width="200" background="<c:out value='${sessionScope.gui_skinPath}'/>/bbs_bg.gif" height="32">
				<span id="currentLocation" class="currentLocation" onclick="jumpToLocationInfo(this.innerText)" style="cursor:hand"><%= GlobalValueUtil.getLocation(session,"")%></span>				
			</td>
			 -->
			<td width="150" background="<c:out value='${sessionScope.gui_skinPath}'/>/bbs_bg.gif" height="32">
				<span class="statusBar_ItemType1" id="statusBar_DateTimeInfo" onclick="">&nbsp;</span>					
			</td>
			<%
				String langText = "English";
				if (lang.equals(LanguageUtil.LANG_BIG5))
				{
					langText = "\u7e41\u9ad4\u4e2d\u6587";
				}
				
				//else if (lang.equals(LanguageUtil.LANG_GB))
				//{
					//langText = "\u7b80\u4f53\u4e2d\u6587";
				//}
			%>
			<td width="100" background="<c:out value='${sessionScope.gui_skinPath}'/>/bbs_bg.gif" height="32">
				<span class="statusBar_ItemType1" id="statusBar_LanguageInfo" onmouseover="this.className='statusBar_ItemType2'" onmouseout="this.className='statusBar_ItemType1'" onclick="showLanguage()"><%=langText%></span><%--語系--%>					
			</td>																		
			<td width="14" height="32"><image src="<c:out value='${sessionScope.gui_skinPath}'/>/bbs_right.gif" width="14" height="32"></image></td>
		</tr>
	</table>
</div>    
        
    </td>
  </tr> 
</table>
        
        
<%--SplitLine------------------------------------------------------------------%>
        
        
<%--StatusBar------------------------------------------------------------------%>
        
        
<div id="languageDiv" style="BACKGROUND-COLOR: #3399FF; visibility:hidden; FILTER:progid:DXImageTransform.Microsoft.Shadow(Color=#333333,offX=10,offY=10,direction=120,Strength=5);">
<iframe src="" frameborder="0" style="position:absolute; visibility:inherit; top:0px; left:0px; width:100%; height:100%; z-index:-1;"></iframe>
  <table border="1" cellspacing="0" width="118" height="100%" bordercolorlight="#444444" cellpadding="0" bordercolordark="#FFFFFF" bordercolor="#FFFFFF">
    <tr lang_id="english" class=yellow9 onmouseover=this.className='blue9' onmouseout=this.className='yellow9' onclick="chLanguage(this);">
      <td height="32" align="left" width="114">English</td>
    </tr>
    <tr lang_id="big5" class=yellow9 onmouseover=this.className='blue9' onmouseout=this.className='yellow9' onclick="chLanguage(this);">
      <td height="32" align="left" width="114"><%="\u7e41\u9ad4\u4e2d\u6587"%></td>
    </tr>
     
  </table>
</div>

<script type="text/javascript">

function position_statusbar()
{

}

position_statusbar();

function chLanguage(obj)
{
	var chLanguage = obj.innerText;
	var langId = obj.lang_id;
	var bodyobj = document.body;
	
	document.getElementById('statusBar_LanguageInfo').innerText = chLanguage;	
	toggleLanguage(langId);

	bodyobj.languageStatus = langId;
	hiddenLanguage();

	/*var selId = document.getElementById('menuBar1_DivMenuBar').selid;
	if(selId !=null && selId!="")
	{
		showShadow(selId,'menuBar1');
	}*/
	
	window.workAreaFrame.languageStatus = langId;
	submitSession("gui_languageStatus",langId);
}

function hiddenLanguage()
{
	document.getElementById('languageDiv').style.visibility='hidden';
	//document.getElementById('languageDivShadow').style.visibility='hidden';
}

function showLanguage()
{
   var obj = document.getElementById("statusBar");   
   objRect = GetOffset(obj);
   var width = 118;
   var height = 100;
   var left = document.body.offsetWidth - 140;
   var top = objRect[0] - height;

   var obj = document.getElementById("languageDiv");
   obj.style.position = "absolute";
   obj.style.top = top;
   obj.style.left = left;
   obj.style.width = width;
   obj.style.height = height;
   obj.style.zIndex = 9;	
	
	document.getElementById('languageDiv').style.visibility='visible';
	//document.getElementById('languageDivShadow').style.visibility='visible';
}

function GetOffset(obj) 
{  
	var objTop=obj.offsetTop;  
	var objLeft=obj.offsetLeft;  
	while(obj=obj.offsetParent) 
	{  
		objTop+=obj.offsetTop;  
		objLeft+=obj.offsetLeft;  
	} 
		
	var rec = new Array(2); 
	rec[0]  = objTop; 
	rec[1] = objLeft; 
	return rec ;
}

if(document.getElementById('workAreaFrame'))
{
	document.getElementById('workAreaFrame').attachEvent("onfocus",hiddenLanguage);
}
</script>

<DIV id="divCover" style="">
<iframe src="" frameborder="0" style="position:absolute; visibility:inherit; top:0px; left:0px; width:100%; height:100%; z-index:-1;filter='progid:DXImageTransform.Microsoft.Alpha(style=0,opacity=85)'"></iframe>
<table border="0" cellspacing="0" bordercolor="#111111" width="100%" height="100%" cellpadding="0">
  <tr>
    <td width="100%" height="100%" align="center">
    <table border="0" cellspacing="0" bordercolor="#111111" width="90%" cellpadding="0" height="178">
      <tr>
        <td height="74" align="center">
          <font size="6" face="Arial Black" color="black">:: <ui:LabelTag>transaction</ui:LabelTag> <ui:LabelTag>in_process</ui:LabelTag>, <ui:LabelTag>please_wait</ui:LabelTag>...</font>
        </td>
      </tr>
      <tr>
        <td height="42" align="center">
          <img src="<c:out value='${sessionScope.gui_skinPath}'/>/shownew.gif" width="30" height="23">
        </td>
      </tr>
      <tr>
        <td height="62" align="center">
            <FORM method=post name=proccess>
              <SCRIPT language=javascript>
            	for(i=0;i<30;i++)
            	{
                  document.write("<input class=proccess>");
            	}
	      </SCRIPT>
            </FORM>
        </td>
      </tr>
    </table>
    </td>
  </tr>
</table>
</DIV>
<STYLE>
.proccess { BACKGROUND: #ffffff; BORDER-BOTTOM: 1px solid; BORDER-LEFT: 1px solid; BORDER-RIGHT: 1px solid; BORDER-TOP: 1px solid; HEIGHT: 8px; MARGIN: 3px; WIDTH: 8px}
</STYLE>
<SCRIPT language=JavaScript>
var p=0,j=0;
var backGroundColorArray=new Array("lightskyblue","white");
function proccess()
{
	try
	{
	    document.forms.proccess.elements[p].style.background=backGroundColorArray[j];
	    p+=1;
	    if(p==30)
	    {
	    	p=0;
	    	j=1-j;
	    }
    }
    catch (err)
    {
    	//do nothing
    }
}
setInterval('proccess();',100);

var bw = document.body.clientWidth;
var bh = document.body.clientHeight;

var obj = document.getElementById("divCover");
obj.style.zIndex=20;
obj.style.position = "absolute";
obj.style.top = 0;
obj.style.left = 0;
obj.style.height = "100%";
obj.style.width = bw;
obj.style.visibility = "hidden";
obj.style.cursor = "wait";
</SCRIPT>

<%--Dialog--%>
<DIV id="divDialog" style="position:absolute; top:0; left:0; height:100%; width:102%; visibility:hidden; z-index:20;">
<iframe src="./common/DialogBackground.jsp" frameborder="0" style="position:absolute; visibility:inherit; top:0px; left:0px; width:100%; height:100%; z-index:-1;filter='progid:DXImageTransform.Microsoft.Alpha(style=0,opacity=50)'"></iframe>
<iframe src="" frameborder="0" id="divDialog_frame" marginwidth="0" marginheight="0" style="position:absolute; visibility:inherit; z-index:1; FILTER:progid:DXImageTransform.Microsoft.Shadow(Color=#333333,offX=10,offY=10,direction=120,Strength=5);"></iframe>
<input type="hidden" id="dialogRtnValue" value="">
</DIV>

<iframe id="frameCalendar_2" src="" frameborder="0" style="top:100; left:400; position:absolute; visibility:hidden; z-index:19;filter='progid:DXImageTransform.Microsoft.Alpha(style=0,opacity=0)'"></iframe>
<iframe onblur="closeCalendar();" src="" id="frameCalendar" frameborder="0" marginwidth="0" marginheight="0" style="top:100; left:400; position:absolute; visibility:hidden; z-index:20; FILTER:progid:DXImageTransform.Microsoft.Shadow(Color=#333333,offX=10,offY=10,direction=120,Strength=5);"></iframe>

<DIV id="msgDialog" style="position:absolute; width:223; height:123; top:50; left:100; visibility:hidden; z-index:20;">
<iframe src="" frameborder="0" style="position:absolute; visibility:inherit; top:0px; left:0px; width:100%; height:100%; z-index:-1;filter='progid:DXImageTransform.Microsoft.Alpha(style=0,opacity=0)'"></iframe>
<table onblur="closeMsgDialog();" border="0" cellspacing="0" style="border-collapse: collapse" bordercolor="#111111" width="100%%" id="AutoNumber1" height="100%" cellpadding="0">
  <tr>
    <td width="100%" height="125" background="<c:out value='${sessionScope.gui_skinPath}'/>/test.gif" valign="top" align="center">
    <table border="0" cellspacing="0" style="border-collapse: collapse" bordercolor="#111111" width="95%" height="74%" cellpadding="0">
      <tr style="font-size: 4pt;">
        <td width="100%" height="1"></td>
      </tr>
      <tr>
        <td width="100%" height="100%">
        <table border="1" cellspacing="1" width="100%" height="100%" bordercolorlight="#FFFFFF" bordercolordark="#000000">
          <tr>
            <td width="100%" height="100%">Can not be empty!</td>
          </tr>
        </table>
        </td>
      </tr>
    </table>
    </td>
  </tr>
</table>
</DIV>


<DIV id="submenu_win" CONTENTEDITABLE="false" style="display:none; position:absolute; top:100; left:expression(document.body.offsetWidth-450); height:400px; width:350px; z-index:99; ">
<iframe id="win_frame" winname="" winstate="" wintop="" winleft="" winwidth="" winheight="" marginWidth="" marginHeight="0" frameBorder="0" scrolling="no" src="" style="position:absolute; border:#111111 0px double; width:100%; height:100%;"></iframe>
</div>

<script language="javascript">
document.execCommand("2D-position",false,true);	
var left = 33;
var preIndex = -1;
function hiddenWin()
{
	if(document.getElementById('submenu_win'+preIndex))
	{
		document.getElementById('submenu_win'+preIndex).style.display='none';
		preIndex = -1;
	}
}

function showWin(win_name,url,index)
{
	if(preIndex!=-1) hiddenWin();
	
	//if(document.getElementById('win_frame'+index).winstate!="Y")
	//{
		document.getElementById('win_frame'+index).src = "dragWindowFrame.jsp?win_name="+ win_name +"&win_url="+ url;
	//}
	document.getElementById('win_frame'+index).winstate = "Y";	
	document.getElementById('submenu_win'+index).style.display='block';
	
	preIndex = index;
}

function doMouseOver(obj,i)
{
	obj.style.left = 0;
	obj.style.width = 60;
	obj.style.height = 60;
	
	var nextObj = document.getElementById('item'+(i+1));
	if(nextObj)
	{
		nextObj.style.left = 15;
		nextObj.style.width = 45;
		nextObj.style.height = 45;	
	}
}

function doMouseOut(obj,i)
{
	obj.style.left = left;
	obj.style.width = 34;
	obj.style.height = 34;
	
	var nextObj = document.getElementById('item'+(i+1));
	if(nextObj)
	{
		nextObj.style.left = left;
		nextObj.style.width = 34;
		nextObj.style.height = 34;	
	}	
	
}
</script>
<span id="toolbar" style="display:none; position:absolute; border-right:#111111 1px double; border-left:#111111 1px double; background-color:#93B6D9; top:99px; left:expression(document.body.offsetWidth-44); height:expression(document.getElementById('workAreaFrame').offsetHeight); width:40px; z-index:99;" ></span>
<span id="btnarea" style="display:none; position:absolute; border:#111111 0px double; top:99px; left:expression(document.body.offsetWidth-74); height:expression(document.getElementById('workAreaFrame').offsetHeight); width:80px; z-index:99;"></span>
<span id="winarea"></span>
<span id="info" style="display:none; position:absolute; border:#111111 0px double; top:500px; left:500px; height:100px; width:200px; z-index:100;" >
</span>

</body>
