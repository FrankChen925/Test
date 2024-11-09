<%-- Header---------------------------------------------------------------------
* System Name   :MESware GUI
* Description   :EqpIlluminationMode
* Modification: (Date-Version-Author-Description) 
* Generate by Gui Editor  Version v2.6
*<p>------------------------------------------------------------------------</p>
* 2007.09.13/1.0.1@andrea_syu - Initial Version.
-------------------------------------------------------------------------------%>

<%-- Page ---------------------------------------------------------------------%>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<%-- Import -------------------------------------------------------------------%>
<%@ page import="java.util.*" %>
<%@ page import="tw.com.synergy.mesware.gui.util.*" %>
<%@ page import="tw.com.synergy.mesware.gui.formobj.*" %>
<%@ page import="tw.com.synergy.mesware.util.*" %>

<%-- TagLib -------------------------------------------------------------------%>
<%@ taglib prefix="ui" uri="GUITag" %>
<%@ taglib prefix="c"  uri="http://java.sun.com/jstl/core" %>

<%-- Page Initial -------------------------------------------------------------%>
<%
//Fixed ------------------------------------------------------------------------
	//do init
	GuiUtility.setInitData(pageContext);

	//get info
	String _functionName = GuiUtility.getFunctionName(pageContext);
    String _event = GuiUtility.getEvent(pageContext);
    Logger _log = GuiUtility.getLogger(pageContext);
    String _logId = _log.getLogId();
    String _functionId = GuiUtility.getFunctionId(pageContext);
    
	//set parameter object
	ParamObject paramObject = new ParamObject(pageContext,_functionName,_log,_logId,_event);
//Fixed ------------------------------------------------------------------------
    try
    {
		Initial(paramObject);

        if(_event.equalsIgnoreCase("") || _event.equalsIgnoreCase("init"))
        {
            Event_Initial(paramObject,_functionId);
        }
        else if (_event.equalsIgnoreCase("query"))
        {
        	Event_Query(paramObject);
        }
        

        buildTagData(paramObject,_functionId);
    }
    catch(Exception e)
    {
        _log.fatal(e.getMessage(),e);
    }
%>

<%!
    public void Initial(ParamObject paramObject) throws Exception
    {
		Logger log = paramObject.getLog();
		PageContext pageContext = paramObject.getPageContext();

    	log.debug("[Request]"+GuiUtility.getAllParameter(pageContext).toString());
    }        

    public void Event_Initial(ParamObject paramObject,String functionId) throws Exception
    {
		Logger log = paramObject.getLog();
   		PageContext pageContext = paramObject.getPageContext();		
		HttpSession session = paramObject.getSession();
		String functionName = paramObject.getFunctionName();

    	try
    	{
    		Get_E_Runcard_Fab_Info(paramObject,functionId);
    		Get_E_Runcard_Eqp_Type(paramObject,functionId);
    	}
    	catch(Exception e)
    	{
            log.fatal(e.getMessage(),e);
    	}
    }
    
    public void Get_E_Runcard_Eqp_Type(ParamObject paramObject,String functionId) throws Exception
    {
		Logger log = paramObject.getLog();
   		PageContext pageContext = paramObject.getPageContext();		
		HttpSession session = paramObject.getSession();
		String functionName = paramObject.getFunctionName();
		
		session.removeAttribute(functionName+"_eqp_Type_select");

		TrxInput ti = new TrxInput(paramObject);
		ti.setPluginId("query_module");
		ti.setTransactionName("QueryParameterValue");
		ti.put("parameter_name","e_runcard_eqp_Type");

		TrxOutput to = ServiceRunner.excuteService(ti);
		if (to.isSuccess())
		{
			String parameterValue = GuiUtility.getProperty(to,"parameter_value","");
			ArrayList<String> tmpList = new ArrayList<String>();
			if (parameterValue!=null && parameterValue.length() > 0) {
				String[] values = parameterValue.split(",");
				for(String v : values) {
					tmpList.add(v);
				}
			}
            session.setAttribute(functionName+"_eqp_Type_select",tmpList);
		}
		else
		{
			GuiUtility.showError(paramObject.getPageContext(),to);
		}	
    }    
    
    public void Get_E_Runcard_Fab_Info(ParamObject paramObject,String functionId) throws Exception
    {
		Logger log = paramObject.getLog();
   		PageContext pageContext = paramObject.getPageContext();		
		HttpSession session = paramObject.getSession();
		String functionName = paramObject.getFunctionName();
		
		session.removeAttribute(functionName+"_fab_select");

		TrxInput ti = new TrxInput(paramObject);
		ti.setPluginId("query_module");
		ti.setTransactionName("QueryParameterValue");

		if (functionId.indexOf("8")>=0) ti.put("parameter_name","e_runcard_fab8");
		else if (functionId.indexOf("12")>=0) ti.put("parameter_name","e_runcard_fab12");
		else if (functionId.indexOf("cfg")>=0) ti.put("parameter_name","e_runcard_fab");
		else if (functionId.indexOf("new")>=0) ti.put("parameter_name","e_runcard_fab");

		TrxOutput to = ServiceRunner.excuteService(ti);
		if (to.isSuccess())
		{
			String parameterValue = GuiUtility.getProperty(to,"parameter_value","");
			ArrayList<String> tmpList = new ArrayList<String>();
			if (parameterValue!=null && parameterValue.length() > 0) {
				String[] values = parameterValue.split(",");
				for(String v : values) {
					tmpList.add(v);
				}
			}
            session.setAttribute(functionName+"_fab_select",tmpList);
		}
		else
		{
			GuiUtility.showError(paramObject.getPageContext(),to);
		}	
    }
    
    public List<Map> Event_Query(ParamObject paramObject) throws Exception
    {
		Logger log = paramObject.getLog();
   		PageContext pageContext = paramObject.getPageContext();		
		HttpSession session = paramObject.getSession();
		String functionName = paramObject.getFunctionName();
		List<Map> consumePlanList = new ArrayList();
		List<Map> resultList = new ArrayList();

    	try
    	{
			String fab = GuiUtility.getParameter(pageContext.getRequest(),"fabSelect","");
			String eqpType = GuiUtility.getParameter(pageContext.getRequest(),"eqpTypeSelect","");
			String illuminationName = GuiUtility.getParameter(pageContext.getRequest(),"illuminationName","");
			
    		TrxInput ti = new TrxInput(paramObject);
       		ti.setFunctionId(paramObject.getFunctionId());
       		ti.setFunctionName(paramObject.getFunctionName());
       		ti.setUserId(paramObject.getUserId());
       		ti.setPackageName("tw.com.synergy.mesware.query.e_runcard");       		
    		ti.setTransactionName("QueryIlluminationInfo");    		
    		ti.put("eqp_type",eqpType);
    		ti.put("fab",fab);
    		ti.put("illumination_name",illuminationName);
    		
    		TrxOutput to = ServiceRunner.excuteService(ti);
    		if (to.isSuccess())
    		{
    			resultList = GuiUtility.getPropertyList(to,"illumination_info_list");
    		}
    		
			pageContext.setAttribute("illumination_info_list",resultList);    		
    	}
    	catch(Exception e)
    	{
            log.fatal(e.getMessage(),e);
    	}
    	return consumePlanList;

    }

    public void buildTagData(ParamObject paramObject,String functionId)
    	throws Exception
    {
    	Logger log = paramObject.getLog();
   		PageContext pageContext = paramObject.getPageContext();
   		HttpSession session = paramObject.getSession();
		String functionName = paramObject.getFunctionName();   		
   		
    	try
    	{
  	
			/*[GUIEditor-BuildTagData-Start]*/
			/*GUIEditor tool generate, do not modify or add any code below block.*/


			Text textGroupText = new Text(pageContext,"textGroupText");
			textGroupText.setValue("illuminationName","%");

			Button deleteButton = new Button(pageContext,"deleteButton");
			deleteButton.setValue("delete");
			Button addButton = new Button(pageContext,"addButton");
			addButton.setValue("add");
			Button updateButton = new Button(pageContext,"updateButton");
			updateButton.setValue("update");
			Button queryButton = new Button(pageContext,"queryButton");
			queryButton.setValue("query");

			Select fabSelect = new Select(pageContext,"fabSelect");
			fabSelect.setDisplayOption(new ArrayList());
			fabSelect.setValueOption(new ArrayList());
			fabSelect.setSelectedOption("");
			Select eqpTypeSelect = new Select(pageContext,"eqpTypeSelect");
			eqpTypeSelect.setDisplayOption(new ArrayList());
			eqpTypeSelect.setValueOption(new ArrayList());
			eqpTypeSelect.setSelectedOption("");

			String consumeTableLangText[] = {"fab","eqp_type","illumination_name","illumination_type","lens_na","sigma","is_usable","description","lm_time","lm_user"};
			String consumeTableOrderText[] = {"fab","eqp_type","illumination_name","illumination_type","lens_na","sigma","is_usable","description","lm_time","lm_user"};
			int consumeTableColumnWidth[] = {38,101,140,130,67,62,76,155,203,165};
			Table consumeTable = new Table(pageContext,"consumeTable");
			consumeTable.setOrderText(consumeTableOrderText);
			consumeTable.setColumnWidth(consumeTableColumnWidth);
			consumeTable.setLangText(consumeTableLangText);
			consumeTable.setTableData(GuiUtility.getParameter(pageContext,"illumination_info_list",new ArrayList()));


/*[GUIEditor-BuildTagData-End]*/

			//consumeTable.setTableData(GuiUtility.getParameter(pageContext,"illumination_info_list",new ArrayList()));

			List fabList = GuiUtility.getParameter(session,functionName+"_fab_select",new ArrayList());
			List TypeList = GuiUtility.getParameter(session,functionName+"_eqp_Type_select",new ArrayList());
			
			if (functionId.indexOf("8")>=0)
			{//e_runcard_fab8
				fabSelect.setDisplayOption(fabList);
				fabSelect.setValueOption(fabList);
			}
			else if (functionId.indexOf("12")>=0)
			{//e_runcard_fab12
				fabSelect.setDisplayOption(fabList);
				fabSelect.setValueOption(fabList);
			}
			else if (functionId.indexOf("cfg")>=0)
			{//e_runcard_fab
				fabSelect.setDisplayOption(fabList);
				fabSelect.setValueOption(fabList);
			}
			else if (functionId.indexOf("new")>=0)
			{//e_runcard_fab
				fabSelect.setDisplayOption(fabList);
				fabSelect.setValueOption(fabList);
			}
			
			//e_runcard_eqp_Type	
			eqpTypeSelect.setDisplayOption(TypeList);
			eqpTypeSelect.setValueOption(TypeList);
			//
			fabSelect.bindReqest();
			eqpTypeSelect.bindReqest();
			textGroupText.bindReqest();
    	}
    	catch(Exception e)
    	{
            log.fatal(e.getMessage(),e);
    	}
    }
%>

<%-- HTML Code ----------------------------------------------------------------%>
<ui:HtmlTag>

<%-- JavaScript Functions -----------------------------------------------------%>
<script Language="JavaScript">
function doInit()
{
	enableGUI();
	
	if("<c:out value='${errorCode}'/>" != "")
	{
		showErrorDialog("<c:out value='${errorCode}'/>");
		return;
	}
}

function doQuery()
{
	document.ParameterSpecSetting.action = 'ParameterSpecSetting.jsp';
	document.ParameterSpecSetting._event.value = "query";
	disableGUI();
	document.ParameterSpecSetting.submit();
}

function doUpdate()
{
	var rowData = consumeTable.getRowDataByName();
	var illuminationName = rowData['illumination_name'];
	var fab = rowData['fab'];

	var eqpType = rowData['eqp_type'];
	var illuminationType = rowData['illumination_type'];
	var lensNa = rowData['lens_na'];
	var sigma = rowData['sigma'];
	var isUsable = rowData['is_usable'];
	var description = rowData['description'];

	if(illuminationName == null && fab == null)
	{
		showWarningDialog('W000220');
		return;
	}

	document.ParameterSpecSetting.selectIlluminationName.value = illuminationName;
	document.ParameterSpecSetting.selectWaferSize.value = fab;
	document.ParameterSpecSetting.selectEqpType.value = eqpType;
	document.ParameterSpecSetting.selectIlluminationType.value = illuminationType;
	document.ParameterSpecSetting.selectLensNa.value = lensNa;
	document.ParameterSpecSetting.selectSigma.value = sigma;
	document.ParameterSpecSetting.selectIsUsable.value = isUsable;
	document.ParameterSpecSetting.selectDescription.value = description;

	document.ParameterSpecSetting.modifyEvent.value = "UPDATE";
	document.ParameterSpecSetting.action = "ParameterUpdateSpecSetting.jsp";
	disableGUI();
	document.ParameterSpecSetting.submit();
}

function doDelete()
{
	if (showConfirmDialog('W000020'))
	{
		var rowData = consumeTable.getRowDataByName();
		var illuminationName = rowData['illumination_name'];
		var fab = rowData['fab'];

		var eqpType = rowData['eqp_type'];
		var illuminationType = rowData['illumination_type'];
		var lensNa = rowData['lens_na'];
		var sigma = rowData['sigma'];
		var isUsable = rowData['is_usable'];
		var description = rowData['description'];
		
		if(illuminationName == null && fab == null)
		{
			showWarningDialog('W000220');
			return;
		}

		fab = fab.replace("CF","");

		document.ParameterSpecSetting.selectIlluminationName.value = illuminationName;
		document.ParameterSpecSetting.selectWaferSize.value = fab;
		document.ParameterSpecSetting.selectEqpType.value = eqpType;
		document.ParameterSpecSetting.selectIlluminationType.value = illuminationType;
		document.ParameterSpecSetting.selectLensNa.value = lensNa;
		document.ParameterSpecSetting.selectSigma.value = sigma;
		document.ParameterSpecSetting.selectIsUsable.value = isUsable;
		document.ParameterSpecSetting.selectDescription.value = description;

		document.ParameterSpecSetting.modifyEvent.value = "DELETE";
		document.ParameterSpecSetting.action = "ParameterDeleteSpecSetting.jsp";
		disableGUI();
		document.ParameterSpecSetting.submit();
	}	
}

function doAdd()
{
	document.ParameterSpecSetting.modifyEvent.value = "ADD"
	document.ParameterSpecSetting.action = "ParameterAddSpecSetting.jsp";
	disableGUI();
	document.ParameterSpecSetting.submit();
}

function processAjaxResult(msgId,to)
{
	if (!isSuccess(to))
	{
		var rtnParamList = to.return_parameter_list;
		var message = "";
		if(rtnParamList != null)				
			message = rtnParamList[0].message;			
		if (message.indexOf("ORA-00001") != -1) 
			showErrorDialog("ORA-00001");
		 else 
			showErrorDialog(to.return_code);
		return;
	}
	
	//if(msgId=="getConsumeInfo")
	//{
	//	handleGetConsumeInfo(to);
	//}
	//else 
	if(msgId=="deleteIllumination")
	{
		showSuccessDialog('SYNF000001');
		doQuery();
		enableGUI();
	}
}
/*
function handleGetConsumeInfo(to)
{
	if (! to) return;
	if (! to.consume_plan_list) return;
 	if (to.consume_plan_list.length)
 	{
 		var consumeList = to.consume_plan_list; 	
 						 								
 		for(var i=0;i<consumeList.length;i++)
 		{ 							
 			var rowData = new Array(); 	
 			rowData['upd'] = 'U';
 			rowData['del'] = 'D';				
 			rowData['product_name'] = consumeList[i].product_name;					
 			rowData['route_name'] = consumeList[i].route_name;
 			rowData['subroute_name'] = consumeList[i].subroute_name; 					 	
 			rowData['step_name'] = consumeList[i].step_name;
 			rowData['eqp_id'] = consumeList[i].eqp_id;
 			rowData['material_part'] = consumeList[i].material_part;
 			rowData['material_check_type'] = consumeList[i].material_check_type;
 			rowData['consume_unit'] = consumeList[i].consume_unit;
 			rowData['consume_qty'] = consumeList[i].consume_qty;
 			rowData['mat_comment'] = consumeList[i].mat_comment;
 			rowData['lm_time'] = consumeList[i].lm_time;								 										
 			rowData['lm_user'] = consumeList[i].lm_user;
 			rowData['consume_qty_type'] = consumeList[i].consume_qty_type;
			consumeTable.addRow(-1,rowData);
								
			var updIndex = getTableHeaderIndex(consumeTable,"upd");					
			var updUrl = "<a href='javascript:doUpdate();'>U</a>";									
			tab_consumeTable.rows[i+1].cells[updIndex].innerHTML = updUrl;
			
			var delIndex = getTableHeaderIndex(consumeTable,"del");					
			var delUrl = "<a href='javascript:doDelete();'>D</a>";									
			tab_consumeTable.rows[i+1].cells[delIndex].innerHTML = delUrl;
			
 		}  								
 	}			
}
*/
//HotKeyUtility
<%
out.println(HotKeyUtility.getHotKeyJavaScriptHtml(paramObject.getFunctionId(),session));
%>

/**
* JGrid needed this function
*/
function onTableSelected(tableName,rowData,selectIndex,status)
{
} 

</script>
<body CLASS="DocumentBody" onload="toggleLanguageForDoc(document);doInit();" scroll="no">
<%-- Form Session -------------------------------------------------------------%>
<form method="post" action="" name="ParameterSpecSetting">
<input type="hidden" name="_event" value="">
<input type="hidden" name="lmUser" value="">
<!-- input type="hidden" name="productNameValue" value=""-->
<!-- input type="hidden" name="routeNameValue" value=""-->
<!-- input type="hidden" name="stepNameValue" value=""-->
<!-- input type="hidden" name="eqpIdValue" value=""-->
<!-- input type="hidden" name="materialPartValue" value=""-->
<!-- input type="hidden" name="subrouteNameValue" value=""-->


<input type="hidden" name="modifyEvent" value="">
<input type="hidden" name="selectIlluminationName" value="">
<input type="hidden" name="selectWaferSize" value="">
<input type="hidden" name="selectEqpType" value="">
<input type="hidden" name="selectIlluminationType" value="">
<input type="hidden" name="selectLensNa" value="">
<input type="hidden" name="selectSigma" value="">
<input type="hidden" name="selectIsUsable" value="">
<input type="hidden" name="selectDescription" value="">


<%--[GUIEditor-Table-Start]--%>
<%--GUIEditor tool generate, do not modify or add any code below block.--%>

<table border='0' cellspacing='0' cellpadding='0' style="table-layout: fixed" width="1200" align="center">
	<tr>
		<td width="12" ></td>
		<td width="6" ></td>
		<td width="212" ></td>
		<td width="143" ></td>
		<td width="6" ></td>
		<td width="143" ></td>
		<td width="6" ></td>
		<td width="143" ></td>
		<td width="293" ></td>
		<td width="25" ></td>
		<td width="206" ></td>
	</tr>
	<tr>
		<td colspan="11" height="12"></td>
	</tr>
	<tr>
		<td height="75"></td>
		<td colspan="8" height="75">
			<fieldset class="CommandFieldSet" style="height:73">
			<legend>
			<ui:LabelTag>
			  condition
			</ui:LabelTag>
			</legend>

			<table border='0' cellspacing='0' cellpadding='0' style="table-layout: fixed; position:relative;left:0px;top:-23px" width="956" align="center">
				<tr>
					<td width="18" ></td>
					<td width="50" ></td>
					<td width="131" ></td>
					<td width="25" ></td>
					<td width="100" ></td>
					<td width="131" ></td>
					<td width="25" ></td>
					<td width="137" ></td>
					<td width="168" ></td>
					<td width="12" ></td>
					<td width="143" ></td>
					<td width="12" ></td>
				</tr>
				<tr>
					<td colspan="12" height="31"></td>
				</tr>
				<tr>
					<td height="25"></td>
					<td height="25">
						<ui:LabelTag  >
							fab
						</ui:LabelTag>
					</td>
					<td height="25">
						<ui:Select name="fabSelect">
							<select style="width:100%">
							</select>
						</ui:Select>
					</td>
					<td height="25"></td>
					<td height="25">
						<ui:LabelTag  >
							eqp_type(%)
						</ui:LabelTag>
					</td>
					<td height="25">
						<ui:Select name="eqpTypeSelect">
							<select style="width:100%">
							</select>
						</ui:Select>
					</td>
					<td height="25"></td>
					<td height="25">
						<ui:LabelTag  >
							illumination_name
						</ui:LabelTag>
					</td>
					<td height="25">
						<ui:TextCol name="textGroupText" textKey="illuminationName">
							<input type="text" style="width:100%" class="CommandText" />
						</ui:TextCol>
					</td>
					<td height="25"></td>
					<td height="25">
						<ui:ButtonTag name="queryButton">
						  <input class="CommandButton" type="button" value="query" onClick="doQuery();"/>
						</ui:ButtonTag>
					</td>
					<td height="25"></td>
				</tr>
				<tr>
					<td colspan="12" height="18"></td>
				</tr>
			</table>
			
			</fieldset>
		</td>
		<td colspan="2" height="75"></td>
	</tr>
	<tr>
		<td colspan="11" height="6"></td>
	</tr>
	<tr>
		<td colspan="3" height="25"></td>
		<td height="25">
			<ui:ButtonTag name="addButton">
			  <input class="CommandButton" type="button" value="add" onClick="doAdd();"/>
			</ui:ButtonTag>
		</td>
		<td height="25"></td>
		<td height="25">
			<ui:ButtonTag name="updateButton">
			  <input class="CommandButton" type="button" value="update" onClick="doUpdate();"/>
			</ui:ButtonTag>
		</td>
		<td height="25"></td>
		<td height="25">
			<ui:ButtonTag name="deleteButton">
			  <input class="CommandButton" type="button" value="delete" onClick="doDelete();"/>
			</ui:ButtonTag>
		</td>
		<td colspan="3" height="25"></td>
	</tr>
	<tr>
		<td height="350"></td>
		<td colspan="8" height="350">
			<fieldset class="CommandFieldSet" style="height:348">
			<legend>
			<ui:LabelTag>
			  consume_plan_1
			</ui:LabelTag>
			</legend>

			<table border='0' cellspacing='0' cellpadding='0' style="table-layout: fixed; position:relative;left:0px;top:-23px" width="956" align="center">
				<tr>
					<td width="12" ></td>
					<td width="931" ></td>
					<td width="12" ></td>
				</tr>
				<tr>
					<td colspan="3" height="25"></td>
				</tr>
				<tr>
					<td height="312"></td>
					<td height="312">
						<fieldset class="CommandTable" style="width:100%;height:310px">
							<ui:Table name="consumeTable" formName="ParameterSpecSetting" hasCheckBox="" disableSort=""/>
						</fieldset>
					</td>
					<td height="312"></td>
				</tr>
				<tr>
					<td colspan="3" height="12"></td>
				</tr>
			</table>
			
			</fieldset>
		</td>
		<td colspan="2" height="350"></td>
	</tr>
	<tr>
		<td colspan="2" height="75"></td>
		<td colspan="8" height="75">
			<ui:ExtendCode name="extendcode1ExtendCode">
			<%=HotKeyUtility.getHotKeyButtonHtml(paramObject.getFunctionId(),session) %>
			</ui:ExtendCode>
		</td>
		<td height="75"></td>
	</tr>
	<tr>
		<td colspan="11" height="356"></td>
	</tr>
</table>
<%--[GUIEditor-Table-End]--%>
</form>
</body>
</ui:HtmlTag>

<%--[GUIEditor-XML-Start]<trx><size_radio>0.8</size_radio><comp_infos><comp_info><isEnable>Y</isEnable><x>15</x><w>780</w><comp_type>12</comp_type><h>60</h><NAME>extendcode1</NAME>
<y>375</y></comp_info><comp_info><On_Blur></On_Blur><isEnable>Y</isEnable><On_MouseUp></On_MouseUp><On_Click>doDelete();</On_Click><On_Focus></On_Focus>
<h>20</h><VALUE>delete</VALUE><CSS_TYPE>Normal</CSS_TYPE><y>75</y><x>425</x><On_MouseDown></On_MouseDown><w>115</w>
<comp_type>2</comp_type><NAME>delete</NAME></comp_info><comp_info><On_Blur></On_Blur><isEnable>Y</isEnable><On_MouseUp></On_MouseUp><On_Click>doAdd();</On_Click><On_Focus></On_Focus>
<h>20</h><VALUE>add</VALUE><CSS_TYPE>Normal</CSS_TYPE><y>75</y><x>185</x><On_MouseDown></On_MouseDown><w>115</w>
<comp_type>2</comp_type><NAME>add</NAME></comp_info><comp_info><On_Blur></On_Blur><isEnable>Y</isEnable><On_MouseUp></On_MouseUp><On_Click>doUpdate();</On_Click><On_Focus></On_Focus>
<h>20</h><VALUE>update</VALUE><CSS_TYPE>Normal</CSS_TYPE><y>75</y><x>305</x><On_MouseDown></On_MouseDown><w>115</w>
<comp_type>2</comp_type><NAME>update</NAME></comp_info><comp_info><COLUMN_WIDTH>31,81,112,104,54,50,61,124,163,132</COLUMN_WIDTH><isEnable>Y</isEnable><HAS_CHECK_BOX></HAS_CHECK_BOX>
<h>250</h><VALUE></VALUE><VALUE_FROM>PageContext</VALUE_FROM><COLUMN_TEXT>fab,eqp_type,illumination_name,illumination_type,lens_na,sigma,is_usable,description,lm_time,lm_user</COLUMN_TEXT><y>115</y>
<x>20</x><w>745</w><DISABLE_SORT></DISABLE_SORT><comp_type>6</comp_type><LANG_TEXT>fab,eqp_type,illumination_name,illumination_type,lens_na,sigma,is_usable,description,lm_time,lm_user</LANG_TEXT><NAME>consume</NAME>
</comp_info><comp_info><isEnable>Y</isEnable><x>10</x><w>765</w><comp_type>7</comp_type><h>280</h><FIELD_SET_TITLE_VALUE>consume_plan_1</FIELD_SET_TITLE_VALUE>
<y>95</y></comp_info><comp_info><On_KeyDown></On_KeyDown><KEY>illumination_name</KEY><READONLY></READONLY><DIGIT></DIGIT>
<On_Change></On_Change><VALUE>%</VALUE><VALUE_FROM>String</VALUE_FROM><y>35</y><x>505</x><w>135</w>
<On_Blur></On_Blur><CSS_ClassName></CSS_ClassName><comp_type>1</comp_type><CALDENDAR></CALDENDAR><On_KeyUp></On_KeyUp>
<h>20</h><MAX_LENGTH></MAX_LENGTH><On_Focus></On_Focus><On_Select></On_Select><On_KeyPress></On_KeyPress><On_Click></On_Click>
<isEnable>Y</isEnable></comp_info><comp_info><COLOR></COLOR><isEnable>Y</isEnable><h>20</h><y>35</y><x>190</x><TEXT>eqp_type(%)</TEXT><w>80</w>
<comp_type>0</comp_type><NAME></NAME></comp_info><comp_info><COLOR></COLOR><isEnable>Y</isEnable><h>20</h><y>35</y><x>25</x><TEXT>fab</TEXT><w>40</w>
<comp_type>0</comp_type><NAME></NAME></comp_info><comp_info><On_Blur></On_Blur><DISPLAY_VALUE></DISPLAY_VALUE><isEnable>Y</isEnable><DISPLAY_VALUE_FROM></DISPLAY_VALUE_FROM><On_Focus></On_Focus>
<h>20</h><VALUE></VALUE><VALUE_FROM></VALUE_FROM><On_Change></On_Change><y>35</y><x>65</x>
<w>105</w><comp_type>5</comp_type><NAME>fab</NAME></comp_info><comp_info><On_Blur></On_Blur><isEnable>Y</isEnable><On_MouseUp></On_MouseUp><On_Click>doQuery();</On_Click><On_Focus></On_Focus>
<h>20</h><VALUE>query</VALUE><CSS_TYPE>Normal</CSS_TYPE><y>35</y><x>650</x><On_MouseDown></On_MouseDown><w>115</w>
<comp_type>2</comp_type><NAME>query</NAME></comp_info><comp_info><COLOR></COLOR><isEnable>Y</isEnable><h>20</h><y>35</y><x>395</x><TEXT>illumination_name</TEXT><w>110</w>
<comp_type>0</comp_type><NAME></NAME></comp_info><comp_info><On_Blur></On_Blur><DISPLAY_VALUE></DISPLAY_VALUE><isEnable>Y</isEnable><DISPLAY_VALUE_FROM></DISPLAY_VALUE_FROM><On_Focus></On_Focus>
<h>20</h><VALUE></VALUE><VALUE_FROM></VALUE_FROM><On_Change></On_Change><y>35</y><x>270</x>
<w>105</w><comp_type>5</comp_type><NAME>eqp_type</NAME></comp_info><comp_info><isEnable>Y</isEnable><x>10</x><w>765</w><comp_type>7</comp_type><h>60</h><FIELD_SET_TITLE_VALUE>condition</FIELD_SET_TITLE_VALUE>
<y>10</y></comp_info></comp_infos></trx>[GUIEditor-XML-End]--%>
