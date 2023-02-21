<%-- HTML Code ----------------------------------------------------------------%>
<html>
  <head>
  </head>
<%-- JavaScript Functions -----------------------------------------------------%>
var contextPath="<c:out value='${pageContext.request.contextPath}'/>";
attachEvent('onunload', clearSession);
function clearSession()
{
	var area = document.getElementById('area').value;
	location.href='index.jsp?area='+area+'&clearSession=Y&skin=<c:out value='${skin}'/>';
	mod=0;
	doScreenChange();
}

function doRefresh()
{
	var area = document.getElementById('area').value;
	detachEvent('onunload',clearSession);
	location.href='index.jsp?area='+area+'&skin=<c:out value='${skin}'/>';
}

function doBackHome()
{
	parent.document.getElementById("functionName").innerText = "";
	document.getElementById('workAreaFrame').src = 'MainGui.jsp';
}

function goToLogin()
{
	var area = document.getElementById('area').value;
	var url = contextPath+'/html/default.jsp?area='+area;
	//var url = contextPath+'/html/default_login.jsp?area='+area; //2011.12.23 update by Rebecca for prevent login & logout infinite loop
    window.open(url,"Cynosure","top=0,left=0,width="+(screen.availWidth-10)+",height="+(screen.availHeight-20)+",toolbar=0,menubar=0,location=0,directories=0,status=0,scrollbars=1");
    window.opener=null;
    window.close();	
}

var mode=0;
var old=new Array();

function doScreenChange2()
{
	var titleTr = document.getElementById("titleTR");
	var menuBar1 = document.getElementById("menuBar1");
	var divMenu = document.getElementById("divMenu");
	var divMenu2 = document.getElementById("divMenu2");
	var backButton = document.getElementById("backButton");
	
	divMenu.style.top = 30;
	divMenu2.style.top = 30;
	titleTr.style.display="none";
	backButton.style.display="block";

}
function doScreenChange3()
{
	var titleTr = document.getElementById("titleTR");
	var menuBar1 = document.getElementById("menuBar1");
	var divMenu = document.getElementById("divMenu");
	var divMenu2 = document.getElementById("divMenu2");
	var backButton = document.getElementById("backButton");
	
	divMenu.style.top = 63;
	divMenu2.style.top = 63;
	titleTr.style.display="block";
	backButton.style.display="none";
}

function doScreenChange()
{
	var e = event;
	if(mode==0)
	{
		//doScreenChange2();
		if(typeof document.all!='undefined')
		{
			if(document.body.offsetWidth==screen.availWidth)
			{

			}
			window.moveBy(e.clientX-e.screenX,e.clientY-e.screenY);
			window.resizeBy(screen.availWidth-document.body.offsetWidth,screen.availHeight-document.body.offsetHeight);
		}
		else
		{
			window.moveTo(0,0);
			window.resizeTo(screen.availWidth,screen.availHeight);
			old[0]=window.toolbar.visible;
			old[1]=window.statusbar.visible;
			old[2]=window.menubar.visible;
			window.toolbar.visible=false;
			window.statusbar.visible=false;
			window.menubar.visible=false;
		}
		mode=1;
	}
	else
	{
		//doScreenChange3();
		if(typeof document.all!='undefined')
		{
			window.moveTo(0,0);
			window.resizeTo(screen.availWidth,screen.availHeight);
		}
		else
		{
			window.toolbar.visible=old[0];
			window.statusbar.visible=old[1];
			window.menubar.visible=old[2];
		}
		mode=0;
	}
	return true;
}

var isWorkCount = 0
function doContinueWork()
{
	isWorkCount = 0;
}

function loadPage(name, id, link, title, langName)
{
	//if(obj.link == "") return;
	//alert(id);
	//alert(langName);
	if(link.indexOf("?")>0)
	{
		var linkUrl = link + '&function_name='+ name +'&function_id='+ id +'&isMenu=Y';
	}
	else
	{
		var linkUrl = link + '?function_name='+ name +'&function_id='+ id +'&isMenu=Y';
	}
	top.document.getElementById("workAreaFrame").src=linkUrl;
	parent.document.getElementById("functionName").innerText = langName;
	parent.document.getElementById("functionName").jsxl = langName;
	
	try
	{
		parent.document.getElementById("functionName").big5 = event.srcElement.big5;
		parent.document.getElementById("functionName").english = event.srcElement.english;	
		parent.document.getElementById("functionName").gb = event.srcElement.gb;
		
		var toLang = parent.document.body.languageStatus;
		if(eval("event.srcElement."+toLang))
		{
			parent.document.getElementById("functionName").innerText = eval("event.srcElement."+toLang);	
		}
	}
	catch(e) {}

	//parent.hotKeyFrame.document.HotKey.result.value="ddddd";
	//alert(parent.hotKeyFrame.document.HotKey.result.value="ddddd");
	//alert(top.document.getElementById("hotKeyFrame").src);
	loadRelationItem(id);
	
	loadSubMenu(id);
	

	//parent.hotKeyFrame.document.HotKey.result.value="ddddd";
	//ajaxSendRequest(top.contextPath +"/html/HotKey.jsp");
	
	
}

var ajax_user_id='admin'; 
var ajax_function_id=''; 
var ajax_function_name='index'; 
var ajax_log_id=''; 
var ajax_data_source = "<c:out value='${sessionScope.global_data_source}'/>";
    
function loadSubMenu(id)
{
	ajax_function_id=id; 
    
	var ti = newServiceInput();		
	ti.transaction_name = "QuerySubMenuItem";
	
	var sajax = new SAjax();
	sajax.callServiceTrx(ti,"QuerySubMenuItem");
}

function processAjaxResult(msgId,to)
{
	if (!isSuccess(to))
	{
		showErrorDialog(to.return_code);
		return;
	}	
	
	if (msgId=="QuerySubMenuItem")
	{
		handQuerySubMenuItem(to);
	}	
}

document.onkeydown = function checkKey() 
{ 
	event.keyCode = 0; 
	return false;
	/*
	if(event.keyCode == 8||event.keyCode == 13) return false;
	
	if (event.ctrlKey && event.keyCode == 78)
	{
		event.returnValue = false; 
	}
	*/
	
}


function handQuerySubMenuItem(to)
{
	document.getElementById("btnarea").innerHTML = "";
	document.getElementById("winarea").innerHTML = "";

	if(to==null) return; 
 	if(to.submenu_item_list==null) return;	
 	if(to.submenu_item_list.length)
 	{
 	 	document.getElementById('toolbar').style.display="block";
 		document.getElementById('btnarea').style.display="block";
 	
 		var itemArray = to.submenu_item_list;
 		for(var i=0;i<itemArray.length;i++)
 		{
 			var rowData = new Array();
 					
 			rowData['name'] = itemArray[i].name;
 			rowData['function_id'] = itemArray[i].function_id;
 			rowData['link'] = itemArray[i].link;
 			rowData['title'] = itemArray[i].title;
 			rowData['icon'] = itemArray[i].icon;
 			rowData['width'] = itemArray[i].width;
 			rowData['height'] = itemArray[i].height;
 			
 			var width = "350";
 			var height= "400";
 			
 			if(rowData['width'].length>0) width = rowData['width'];
 			if(rowData['height'].length>0) height = rowData['height'];
 			
 			var left = parseInt(width)+100;
 					
 			var newObj = "<div id='item"+i+"' class='ListItem' ";
 			newObj += "onmouseenter='doMouseOver(this,"+ i +");' onmouseleave='doMouseOut(this,"+ i +");' ";
 			newObj += "style='position:relative; left:33px; BORDER: #0000ff 0px solid; WIDTH: 34px; HEIGHT: 34px; FILTER: progid:DXImageTransform.Microsoft.AlphaImageLoader(src=\"<c:out value='${sessionScope.gui_skinPath}'/>/"+rowData['icon']+"\", sizingMethod=\"scale\"); cursor:hand' ";
 			newObj += "title='"+ rowData['name'] +"' onclick='showWin(\""+ rowData['name'] +"\",\""+ rowData['link']+"\","+ i +")'>";
 			newObj += "</div>";
 			
 			var winObj = "<div winindex=\""+ i +"\" id=\"submenu_win"+i+"\" CONTENTEDITABLE=\"false\" style=\"display:none; position:absolute; top:100; left:expression(document.body.offsetWidth-"+  left +"); height:"+ height +"px; width:"+ width +"px; z-index:99; \">";
			winObj += "<iframe id=\"win_frame"+i+"\" winname=\"\" winstate=\"\" marginWidth=\"0\" marginHeight=\"0\" frameBorder=\"0\" scrolling=\"no\" src=\"\" style=\"position:absolute; border:#111111 0px double; width:100%; height:100%;\"></iframe>";
			winObj += "</div>";
 						
			document.getElementById("btnarea").insertAdjacentHTML('beforeEnd',newObj);
			document.getElementById("winarea").insertAdjacentHTML('beforeEnd',winObj);
 		}	
 	}
	else
 	{
 		document.getElementById('toolbar').style.display="none";
 		document.getElementById('btnarea').style.display="none";
 	}  
}



function jumpToLocationInfo(location)
{   if (location != "" && location != "Location" )
	{
		if (document.getElementById('functionName').jsxl == "Location InLine Information")
		{
			
		}
		else
		{
			loadPage('Location InLine Information','open.system.location','location_info.jsp?location_id=' + location,'','Location InLine Information');	
		}
	}
}

function loadRelationItem(functionId)
{
	var rf = document.getElementById("relationFunction");
	if (rf&&rf.all)
	{
			for(var i=0;i<rf.all.length;i++)
			{
				rf.all[i].style.display='none';
			}
	}
	
	var fids = document.getElementsByName("relation_"+functionId);
	if (fids)
	{
		if (fids.length)
		{
			for(var i=0;i<fids.length;i++)
			{
				fids[i].style.display='inline';
			}
		}
	}
}


</script>
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
					
					
					<!-- 
					<td width="67%" height="26">
						<span style="font-family:Arial Black; color:#585894">-</span>
						<span style="font-family:Arial Black; color:#585894; font-size:12pt;">Cynosure 5</span>
					</td>
					 -->
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
  <!--
  <tr>
    <td width="80%" height="30">
	<%-- MenuBar ------------------------------------------------------------------%>
	<% 
	//StringBuffer relationItemSb = new StringBuffer();
	//buildMenuBar(pageContext,out,session,area,skinPath,relationItemSb); 
	%>
    </td>

  </tr>  
  -->
  <tr>
    <td height="100%" width="100%">
    <table border="0" cellpadding="0" cellspacing="0" style="table-layout:fixed; border-collapse: collapse" bordercolor="#111111" height="100%" width="100%">
      <tr>
       <!-- 
      	<td width="30">
      	
<div id="divMenu" style="position:absolute; top:63; left:-180; width:240; height:635; z-index:5; visibility:hidden;">
<iframe src="" frameborder="0" style="position:absolute; visibility:inherit; top:0px; left:0px; width:100%; height:100%; z-index:-1;"></iframe>
  <table border="1" cellspacing="0" width="100%" height="100%" height="517" bordercolorlight="#444444" cellpadding="0" bordercolordark="#FFFFFF" bordercolor="#FFFFFF">
    <tr>
      <td width="100%" height="24" class="menuTreeHeaderBg" align="left">
      <input type="image" border="0" src="<c:out value='${sessionScope.gui_skinPath}'/>/move_left.gif" width="23" height="23" onclick="moveMenu('left')" class='gray' onMouseOver="this.className=''" onMouseOut="this.className='gray'"></td>
    </tr>
   
    <tr>
      <td height="100%" valign="top">
         <iframe width="100%" height="0" scrolling="auto" frameborder="0" id="menuTreeFrame0" src="perspective_view.jsp"></iframe>
      </td>
    </tr>
    
  </table>
</div>

<div id="divMenu2" style="position:absolute; top:63; left:0; width:30; height:200; z-index:5; visibility:visible; ">
  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse; table-layout: fixed; WORD-BREAK: break-all; WORD-WRAP: break-word;" bordercolor="#111111" width="29">
    <tr style="font-size:0px;">
      <td width="100%" height="11">
      	<img border="0" src="<c:out value='${sessionScope.gui_skinPath}'/>/b_top.jpg" width="29" height="11">
      </td>
    </tr>
    <tr>
      <td width="100%" background="<c:out value='${sessionScope.gui_skinPath}'/>/b_bg2.jpg" height="22" align="center">
      <img src="<c:out value='${sessionScope.gui_skinPath}'/>/p_02.gif" hidefocus width="18" height="18" style="cursor:hand;" onclick="moveMenu('right',null)" onMouseOver="this.src='<c:out value='${sessionScope.gui_skinPath}'/>/p_03.gif'" onMouseOut="this.src='<c:out value='${sessionScope.gui_skinPath}'/>/p_02.gif'">
      </td>
    </tr>
    <tr>
      <td width="100%" height="4">
      <img border="0" src="<c:out value='${sessionScope.gui_skinPath}'/>/b_line.jpg" width="29" height="4"></td>
    </tr>
    <tr>
      <td width="100%" height="130" align="center" background="<c:out value='${sessionScope.gui_skinPath}'/>/b_bg2.jpg">
      <div style="WORD-BREAK: break-all; WORD-WRAP: break-word; font-size:12pt; font-family:Arial Black; color:#2F2F79; width:15px; border:#333333 0px solid; " jsxl="menu" english="Menu" big5="Menu" gb="#menu" >MENU</div>
      </td>
    </tr>
    <tr>
      <td width="100%" height="13">
      <img border="0" src="<c:out value='${sessionScope.gui_skinPath}'/>/b_bottom.jpg" width="29" height="13"></td>
    </tr>
  </table>
</div>     
 	
      	</td>
      	 
        <td width="6"><span id="divSplitBar2" class="splitBar" style="width:6px; height:100%;"></span></td>-->
        <td width="100%">
        <%--Work Area------------------------------------------------------------------%>
<div id="mainWorkArea" class="mainWorkArea">
<table border="0" cellspacing="0" width="100%" height="100%" style="table-layout:fixed;" cellpadding="0" bordercolorlight="#808080" bordercolordark="#FFFFFF">
  <tr>
    <td width="100%" height="4" background="<c:out value='${sessionScope.gui_skinPath}'/>/obj_head_03.gif"></td>
  </tr>
  <input id="functionId" type="hidden" name="" value="">
  <input id="functionUrl" type="hidden" name="" value="">
   <%--
 <tr class="mainPageBg">
    <td width="100%" height="30">
  
      <table border="1" cellspacing="1" style="border-collapse: collapse" bordercolor="#111111" width="100%" height="100%">
        <tr>
          <td class="functionInfoArea" width="30%" align="left">
          	<span id="relationFunction" class="functionName" >						
						<span id='relation_defaultpage' style='display:none;'  onclick="loadPage('Logoff','opn.wip_tracking.logoff','./wip_tracking/Logoff.jsp','Logoff','Logoff');" class='iconBtnType2' onmouseover="this.className='iconBtnType1'" onmouseout="this.className='iconBtnType2'"><input id='relation_defaultpage' type='image' hidefocus src='<c:out value='${sessionScope.gui_skinPath}'/>/function_icon/icon1.gif' width='25' height='25' title='Logoff'></span>
						<span id='relation_defaultpage' style='display:none;'  onclick="loadPage('Logon','opn.wip_tracking.logon','./wip_tracking/LogOn.jsp','Logon','Logon');" class='iconBtnType2' onmouseover="this.className='iconBtnType1'" onmouseout="this.className='iconBtnType2'"><input id='relation_defaultpage' type='image' hidefocus src='<c:out value='${sessionScope.gui_skinPath}'/>/function_icon/icon2.gif' width='25' height='25' title='Logon'></span>
						<span id='relation_opn.system.mask' style='display:none;'  onclick="loadPage('View Mask Information','opn.view.view_mask_information','./view/ViewMaskInformation.jsp','View Mask Information','View Mask Information');" class='iconBtnType2' onmouseover="this.className='iconBtnType1'" onmouseout="this.className='iconBtnType2'"><input id='relation_opn.system.mask' type='image' hidefocus src='<c:out value='${sessionScope.gui_skinPath}'/>/function_icon/icon2.gif' width='25' height='25' title='View Mask Information'></span>
						 <%=relationItemSb%>	           		
          	
          	</span>
          </td>
          <td class="functionInfoArea" width="50%" align="center">
          	<span id="functionName" class="functionName">OMI</span>
          </td>
          <td class="functionInfoArea" width="20%" align="center">
	      	<span id="currentLocation" class="currentLocation" onclick="jumpToLocationInfo(this.innerText)" style="cursor:hand"><%= GlobalValueUtil.getLocation(session,"")%></span>
          </td>
          <td class="functionInfoArea" width="0%" align="center" style="display:none;">
	      	<span id="funInfo3" class="functionName"></span>
          </td>
        </tr>
      </table>
    </td>
  </tr>
  --%>
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
     <%--
    <tr lang_id="gb" class=yellow9 onmouseover=this.className='blue9' onmouseout=this.className='yellow9' onclick="chLanguage(this);">
      <td height="32" align="left" width="114"><%="\u7b80\u4f53\u4e2d\u6587"%></td>
    </tr>
   
    <tr lang_id="jp" class=yellow9 onmouseover=this.className='blue9' onmouseout=this.className='yellow9' onclick="chLanguage(this);">
      <td height="32" align="left" width="114">Japanese</td>
    </tr>    
    <tr lang_id="kor" class=yellow9 onmouseover=this.className='blue9' onmouseout=this.className='yellow9' onclick="chLanguage(this);">
      <td height="32" align="left" width="114">Korean</td>
    </tr>--%>
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

</html>
