import sys
import time

import numpy as np

#pyside2 包的引入需再最前面，否则会报错
from PySide2.QtWidgets import QApplication,QMainWindow
from PySide2.QtUiTools import QUiLoader

from matplotlib.backends.qt_compat import QtCore, QtWidgets

if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure




import PLinApi
import collections
from ctypes import *

"""
lin数据的收发已经做好，待优化
"""


#解析lin信息的类
class MessageStatus:

    """
    Message Status structure used to show LIN Messages in a ListBox.

    Attributes:
        m_Msg           The received LIN message (TLinRcvMsg)
        m_oldTimeStamp  Timestamp of a previously received message (c_uint64)
        m_iIndex        index of the message in the ListView component (int)
        m_Count         Number of LIN message received with the same frame ID (int)
        m_bShowPeriod   Defines if the timestamp is displayed as a period (boolean)
        m_bWasChanged   Defines if the message has been modified
                        and its display needs to be updated (boolean)
    """
    # Constructor
    #

    def __init__(self, linMsg, listIndex):
        """
        Creates a new MessageStatus object

        Parameters:
            linMsg      received LIN message (TLinRcvMsg)
            listIndex   index of the message in the ListView
        """
        self.m_Msg = linMsg
        self.m_oldTimeStamp = linMsg.TimeStamp
        self.m_iIndex = listIndex
        self.m_Count = 1
        self.m_bShowPeriod = True
        self.m_bWasChanged = False

    # Updates an existing MessageStatus with a new LIN message
    #
    def update(self, linMsg):
        """
        Updates an existing MessageStatus with a new LIN message.

        Parameters:
            linMsg LIN message to update (TLINRcvMsg)
        """
        self.m_oldTimeStamp = self.m_Msg.TimeStamp
        self.m_Msg = linMsg
        self.m_Count += 1
        self.m_bWasChanged = True

    # States wether the timestamp is displayed as a period or not
    #
    def setShowPeriod(self, value):
        """
        States wether the timestamp is displayed as a period or not

        Parameters:
            value True if the period should be displayed, False for the timestamp
        """
        if (self.m_bShowPeriod ^ value):
            self.m_bShowPeriod = value
            self.m_bWasChanged = True

    # Returns the timestamp or the period of the frame
    #
    def getTimeString(self):
        """
        Returns the timestamp or the period of the frame.

        Returns:
            timestamp or period in milliseconds
        """
        time = self.m_Msg.TimeStamp
        if (self.m_bShowPeriod):
            time = (time - self.m_oldTimeStamp) / 1000
        return str(time)

    # Formats Data field as string
    #
    def getDataString(self):
        """
        Formats Data field as string

        Returns:
            None
        """
        dataStr = ""
        for i in range(self.m_Msg.Length):
            # data item to hex
            data = hex(self.m_Msg.Data[i])
            # remove first '0b' character and pad with '0'
            data = data[2:].zfill(2)
            # format
            dataStr = str.format("{0}{1} ", dataStr, data)

        # remove ending space
        dataStr = dataStr[:-1]
        return dataStr

    # Formats LIN message (m_Msg) Error field as string
    #
    def getErrorString(self):
        """
        Formats LIN message (m_Msg) Error field as string.

        Returns:
            Error field as string
        """
        error = ""
        if (self.m_Msg.ErrorFlags & PLinApi.TLIN_MSGERROR_CHECKSUM):
            error = error + 'Checksum,'
        if (self.m_Msg.ErrorFlags & PLinApi.TLIN_MSGERROR_GROUND_SHORT):
            error = error + 'GroundShort,'
        if (self.m_Msg.ErrorFlags & PLinApi.TLIN_MSGERROR_ID_PARITY_BIT_0):
            error = error + 'IdParityBit0,'
        if (self.m_Msg.ErrorFlags & PLinApi.TLIN_MSGERROR_ID_PARITY_BIT_1):
            error = error + 'IdParityBit1,'
        if (self.m_Msg.ErrorFlags & PLinApi.TLIN_MSGERROR_INCONSISTENT_SYNCH):
            error = error + 'InconsistentSynch,'
        if (self.m_Msg.ErrorFlags & PLinApi.TLIN_MSGERROR_OTHER_RESPONSE):
            error = error + 'OtherResponse,'
        if (self.m_Msg.ErrorFlags & PLinApi.TLIN_MSGERROR_SLAVE_NOT_RESPONDING):
            error = error + 'SlaveNotResponding,'
        if (self.m_Msg.ErrorFlags & PLinApi.TLIN_MSGERROR_SLOT_DELAY):
            error = error + 'SlotDelay,'
        if (self.m_Msg.ErrorFlags & PLinApi.TLIN_MSGERROR_TIMEOUT):
            error = error + 'Timeout,'
        if (self.m_Msg.ErrorFlags & PLinApi.TLIN_MSGERROR_VBAT_SHORT):
            error = error + 'VBatShort,'
        if (self.m_Msg.ErrorFlags == 0):
            error = 'O.k. '
        # remove ending comma
        error = error[:-1]
        return error


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()

        #GUI 动态载入
        self.ui = QUiLoader().load('u1.ui')


        """
        layout = self.ui.HLayout_showpic

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))

        layout.addWidget(static_canvas)

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")
        """
        layout = self.ui.HLayout_showpic
        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(dynamic_canvas)

        self.addToolBar(NavigationToolbar(dynamic_canvas, self))

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        t = np.linspace(0, 10, 101)
        # Set up a Line2D.
        self._line, = self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._timer = dynamic_canvas.new_timer(50)
        self._timer.add_callback(self._update_canvas)
        self._timer.start()
        #self.ui.addToolBar(NavigationToolbar(static_canvas, self))
        #Lin通讯有关参数初始化
        self.hardwareInit()

        #部件逻辑初始化
        self.widgetsInit()

    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._line.set_data(t, np.sin(t + time.time()))
        self._line.figure.canvas.draw()

    def test(self):

        pass

    def readtest(self):
        print('read button pressed down')
        self.readMsgSend()

    def widgetsInit(self):
        #按键按下逻辑

        #读取信息按键被按下
        self.ui.pushBtn_Linread.clicked.connect(self.readtest)

        #显示读取的信息按下
        self.ui.pushBtn_showmsg.clicked.connect(self.readMessages)

        #刷新动作
        self.ui.pushBtn_refresh.clicked.connect(self.refreshHardware)

        self.ui.cbBox_hardware.activated.connect(self.test)

        #连接动作，断开
        self.ui.pushBtn_connect.clicked.connect(self.linConnect)
        self.ui.pushBtn_disconnect.clicked.connect(self.doLinDisconnect)

        #车窗运动命令
        self.ui.radioBtn_manualup.toggled.connect(self.linMsgSend)
        self.ui.radioBtn_manualdown.toggled.connect(self.linMsgSend)
        self.ui.radioBtn_autoup.toggled.connect(self.linMsgSend)
        self.ui.radioBtn_autodown.toggled.connect(self.linMsgSend)
        self.ui.radioBtn_nocmd.toggled.connect(self.linMsgSend)

    def hardwareInit(self):


        # 创建一个实例 自动load PLIN-API
        self.m_objPLinApi = PLinApi.PLinApi()
        if (not self.m_objPLinApi.isLoaded()):
            print("当前目录下没有dll文件，加载失败")
            raise Exception("PLin-API could not be loaded ! Exiting...")

        # configure LIN variables
        self.m_hClient = PLinApi.HLINCLIENT(0)
        self.m_hHw = PLinApi.HLINHW(0)
        self.m_HwMode = PLinApi.TLIN_HARDWAREMODE_NONE
        self.m_HwBaudrate = c_ushort(0)
        self.FRAME_FILTER_MASK = c_uint64(0xFFFFFFFFFFFFFFFF)
        self.m_lMask = self.FRAME_FILTER_MASK

        # LIN GUI variables

        # sorted dictionnary of available hardware
        d = {'<No available harware>': PLinApi.HLINHW(0)}
        self.m_dataHws = collections.OrderedDict(
            sorted(list(d.items()), key=lambda t: t[0]))
        self.ui.cbBox_hardware.addItem('<No available harware>')
        self.ui.cbBox_hardware.setCurrentIndex(0)

        # sorted dictionnary of hardware baudrates
        d = {'2400': 2400, '9600': 9600, '10400': 10400, '19200': 19200}
        self.m_dataHwBaudrates = collections.OrderedDict(
            sorted(list(d.items()), key=lambda t: t[1]))
        for name in self.m_dataHwBaudrates.keys():
            self.ui.cbBox_buadrate.addItem(name)
        self.ui.cbBox_buadrate.setCurrentIndex(3)

        # sorted dictionary of hardware mode
        d = {'Master': PLinApi.TLIN_HARDWAREMODE_MASTER,
             'Slave': PLinApi.TLIN_HARDWAREMODE_SLAVE}
        self.m_dataHwModes = collections.OrderedDict(
            sorted(list(d.items()), key=lambda t: t[0]))
        for name in self.m_dataHwModes.keys():
            self.ui.cbBox_mode.addItem(name)
        self.ui.cbBox_mode.setCurrentIndex(0)
        # LIN Global Frame Table
        '''
        self.m_pGFT = CGlobalFrameTable(
            self.m_objPLinApi, self.m_hClient, self.m_hHw, self.m_HwMode, self.m_lMask)
            '''
        # LIN message receive queue
        #lin 读取信息接收缓冲列表
        self.m_LastMsgsList = []

    def refreshHardware(self):
        """
        Fills combobox  with available LIN hardware

        Returns:
            None
        """
        # Get the buffer length needed...
        lwCount = c_ushort(0)
        availableHWs = (PLinApi.HLINHW * 0)()
        linResult = self.m_objPLinApi.GetAvailableHardware(availableHWs, 0, lwCount)
        if (lwCount == 0):
            # use default value if either no hw is connected or an unexpected error occured
            lwCount = c_ushort(16);
        availableHWs = (PLinApi.HLINHW * lwCount.value)()
        lwBuffSize = c_ushort(lwCount.value * 2)

        # Get all available LIN hardware.
        linResult = self.m_objPLinApi.GetAvailableHardware(
            availableHWs, lwBuffSize, lwCount)
        '''
        获取可用的硬件信息
        '''
        if (linResult == PLinApi.TLIN_ERROR_OK):

            # clear combobox
            self.ui.cbBox_hardware.clear()
            self.m_dataHws.clear()

            # Get information for each LIN hardware found
            lnHwType = c_int(0)
            lnDevNo = c_int(0)
            lnChannel = c_int(0)
            lnMode = c_int(0)

            #把硬件信息加入下拉框中
            if (lwCount.value == 0):
                '''
                如果没发现可用的硬件连接
                '''
                strHw = '<No Hardware found>'
                self.ui.cbBox_hardware.addItem(strHw)
                self.m_dataHws[strHw] = PLinApi.HLINHW(0)
            else:
                self.ui.pushBtn_connect.setEnabled(True)
                for i in range(lwCount.value):

                    lwHw = availableHWs[i]

                    # Read the type of the hardware with the handle lwHw.
                    self.m_objPLinApi.GetHardwareParam(
                        lwHw, PLinApi.TLIN_HARDWAREPARAM_TYPE, lnHwType, 0)

                    # Read the device number of the hardware with the handle
                    # lwHw.
                    self.m_objPLinApi.GetHardwareParam(
                        lwHw, PLinApi.TLIN_HARDWAREPARAM_DEVICE_NUMBER, lnDevNo, 0)

                    # Read the channel number of the hardware with the handle
                    # lwHw.
                    self.m_objPLinApi.GetHardwareParam(
                        lwHw, PLinApi.TLIN_HARDWAREPARAM_CHANNEL_NUMBER, lnChannel, 0)

                    # Read the mode of the hardware with the handle lwHw (Master,
                    # Slave or None).
                    self.m_objPLinApi.GetHardwareParam(
                        lwHw, PLinApi.TLIN_HARDWAREPARAM_MODE, lnMode, 0)
                    #没有连接 所以读取的信息是没有模式的
                    #print(lnMode.value)

                    # translate type value to string
                    if (lnHwType.value == PLinApi.LIN_HW_TYPE_USB_PRO.value):
                        strName = "PCAN-USB Pro"
                    elif (lnHwType.value == PLinApi.LIN_HW_TYPE_USB_PRO_FD.value):
                        strName = "PCAN-USB Pro FD"
                    elif (lnHwType.value == PLinApi.LIN_HW_TYPE_PLIN_USB.value):
                        strName = "PLIN-USB"
                    else:
                        strName = "Unknown"

                    # add information to channel combobox
                    strHw = str.format(
                        '{0} - dev. {1}, chan. {2}', strName, lnDevNo.value, lnChannel.value)
                    self.ui.cbBox_hardware.addItem(strHw)

                    '''
                    这里很重要,把可连接的硬件名字 存入数组
                    '''
                    self.m_dataHws[strHw] = PLinApi.HLINHW(lwHw)
            # select first item
            self.ui.cbBox_hardware.setCurrentIndex(0)
            print(self.ui.cbBox_hardware.currentText())
        else:
            print('调用PlinApi函数失败！')

    def readMsgSend(self):
        '''
        发送，master 模式，帧ID 31,数据域8字节
        '''

        pMsg = PLinApi.TLINMsg()

        #此处为PID 不是帧ID 对应帧ID 31
        pMsg.FrameId = c_ubyte(177)
        #2 为subscriber
        pMsg.Direction = PLinApi.TLINDirection(2)
        #2  为enhanced type
        pMsg.ChecksumType = PLinApi.TLINChecksumType(2)

        #3 数据域长度先定位8
        pMsg.Length = c_ubyte(8)

        self.m_Data0TXT = '00'
        self.m_Data1TXT = '00'
        self.m_Data2TXT = '00'
        self.m_Data3TXT = '00'
        self.m_Data4TXT = '00'
        self.m_Data5TXT = '00'
        self.m_Data6TXT = '00'
        self.m_Data7TXT = '00'

        # fill data
        edits = [
            self.m_Data0TXT, self.m_Data1TXT, self.m_Data2TXT, self.m_Data3TXT,
            self.m_Data4TXT, self.m_Data5TXT, self.m_Data6TXT, self.m_Data7TXT]

        #不超过上限 0~7
        #转换为由16进制转为10进制整形
        for i in range(0,8):
            pMsg.Data[i] = c_ubyte(int(edits[i], 16))
            #print(pMsg.Data[i])

        # Check if the hardware is initialized as master
        if (self.m_HwMode.value == PLinApi.TLIN_HARDWAREMODE_MASTER.value):
            # Calculate the checksum contained with the
            # checksum type that was set some line before.
           # print('send')
            linResult = self.m_objPLinApi.CalculateChecksum(pMsg)
          #  print(linResult)
            # Try to send the LIN frame message with LIN_Write.
            linResult = self.m_objPLinApi.Write(self.m_hClient, self.m_hHw, pMsg)

    def linMsgSend(self):
        """
        ComboBox cbbID selection changed handler

        Returns:
            None
        """
        # Assert that a frame ID has been selected
        # Get the CFrameDefinition associated to the selected FrameID

        '''
        frame = None
        try:
            frameId = int(self.cbbID['selection'], 16)
            frame = self.m_pGFT.m_lFrameDefinitions[frameId]
        except:
            self.cbbID.focus()
            return
        '''

        '''
        发送，master 模式，帧ID 1c,数据域8字节
        '''

        pMsg = PLinApi.TLINMsg()

        #此处为PID 不是帧ID 对应帧ID 1C
        pMsg.FrameId = c_ubyte(156)
        pMsg.Direction = PLinApi.TLINDirection(1)
        pMsg.ChecksumType = PLinApi.TLINChecksumType(2)
        pMsg.Length = c_ubyte(8)

        if(self.ui.radioBtn_autodown.isChecked()):
            self.m_Data2TXT = '40'
        elif(self.ui.radioBtn_manualup.isChecked()):
            self.m_Data2TXT = '10'
        elif(self.ui.radioBtn_manualdown.isChecked()):
            self.m_Data2TXT = '20'
        elif(self.ui.radioBtn_autoup.isChecked()):
            self.m_Data2TXT = '30'
        elif(self.ui.radioBtn_nocmd.isChecked()):
            self.m_Data2TXT = '00'
        else:
            self.m_Data2TXT = '00'

        self.m_Data0TXT = '00'
        self.m_Data1TXT = '00'
       # self.m_Data2TXT = '10'
        self.m_Data3TXT = '00'
        self.m_Data4TXT = '00'
        self.m_Data5TXT = '11'
        self.m_Data6TXT = '00'
        self.m_Data7TXT = '00'

        # fill data
        edits = [
            self.m_Data0TXT, self.m_Data1TXT, self.m_Data2TXT, self.m_Data3TXT,
            self.m_Data4TXT, self.m_Data5TXT, self.m_Data6TXT, self.m_Data7TXT]

        #不超过上限 0~7
        #转换为由16进制转为10进制整形
        for i in range(0,8):
            pMsg.Data[i] = c_ubyte(int(edits[i], 16))
            #print(pMsg.Data[i])

        # Check if the hardware is initialized as master
        if (self.m_HwMode.value == PLinApi.TLIN_HARDWAREMODE_MASTER.value):
            # Calculate the checksum contained with the
            # checksum type that was set some line before.
           # print('send')
            linResult = self.m_objPLinApi.CalculateChecksum(pMsg)
          #  print(linResult)
            # Try to send the LIN frame message with LIN_Write.
            linResult = self.m_objPLinApi.Write(self.m_hClient, self.m_hHw, pMsg)
           # print(linResult)

    def linConnect(self):
        """
        Connects to a LIN hardware.

        Returns:
            True if connection is successful, False otherwise
        """
        result = False
        if (self.m_hHw.value != 0):
            # If a connection to hardware already exits
            # disconnect this connection first.
            if (not self.doLinDisconnect()):
                print('Link is already existing')
                return result

        if (self.m_hClient.value == 0):
            # register LIN client
            self.m_objPLinApi.RegisterClient(
                "PLIN-API Example", None, self.m_hClient)

        # Try to connect the application client to the hardware with the local
        # handle.
        #当前选中要连接的硬件型号
        hwHandle = self.m_dataHws[self.ui.cbBox_hardware.currentText()]
        #开始连接
        linResult = self.m_objPLinApi.ConnectClient(self.m_hClient, hwHandle)

        if (linResult == PLinApi.TLIN_ERROR_OK):

            self.ui.groupBox_Action.setEnabled(True)
            # If the connection successfull assign
            # the local handle to the member handle.
            self.m_hHw = hwHandle
           # print('lianjiechengg')
            # read hardware's parameter mode and baudrate
            lnMode = c_int(0)
            lnCurrBaud = c_int(0)
            linResult = self.m_objPLinApi.GetHardwareParam(
                hwHandle, PLinApi.TLIN_HARDWAREPARAM_MODE, lnMode, 0)
            linResult = self.m_objPLinApi.GetHardwareParam(
                hwHandle, PLinApi.TLIN_HARDWAREPARAM_BAUDRATE, lnCurrBaud, 0)

            # check if initialization is required
            #Mode selection Master or slave
            #注意这里是字典，键为字符
            hwMode = self.m_dataHwModes[self.ui.cbBox_mode.currentText()]

            #baudrate selection
            try:
                # convert baudrates selection to int
                hwBaudrate = c_ushort(int(self.ui.cbBox_buadrate.currentText()))
            except:
                hwBaudrate = c_ushort(0)

            if (lnMode.value == PLinApi.TLIN_HARDWAREMODE_NONE.value or lnCurrBaud.value != hwBaudrate.value):
                # Only if the current hardware is not initialized
                # try to Initialize the hardware with mode and baudrate
                linResult = self.m_objPLinApi.InitializeHardware(
                    self.m_hClient, self.m_hHw, hwMode, hwBaudrate)
                #print('连接成功')

            if (linResult == PLinApi.TLIN_ERROR_OK):
                self.m_HwMode = hwMode
                self.m_HwBaudrate = hwBaudrate
                # Set the client filter with the mask.
                #print('ewerwer')
                linResult = self.m_objPLinApi.SetClientFilter(
                    self.m_hClient, self.m_hHw, self.m_lMask)
                # Read the frame table from the connected hardware.
                # self.readFrameTableFromHw()
                # Reset the last LIN error code to default.
                linResult = PLinApi.TLIN_ERROR_OK
                result = True
            else:
                # An error occured while initializing hardware.
                # Set the member variable to default.
                self.m_hHw = PLinApi.HLINHW(0)
                result = False
        else:
            # The local hardware handle is invalid
            # and/or an error occurs while connecting
            # hardware with client.
            # Set the member variable to default.
            self.m_hHw = PLinApi.HLINHW(0)
            result = False
        if (linResult != PLinApi.TLIN_ERROR_OK):
            self.showMessageError(linResult)
        return result

    # Disconnects an existing connection to a LIN hardware

    def doLinDisconnect(self):
        # If the application was registered with LIN as client.
        if (self.m_hHw.value != 0):
            # The client was connected to a LIN hardware.
            # Before disconnect from the hardware check
            # the connected clients and determine if the
            # hardware configuration have to reset or not.
            #
            # Initialize the locale variables.
            lfOtherClient = False
            lfOwnClient = False
            lhClientsSize = c_ushort(255)
            lhClients = (PLinApi.HLINCLIENT * lhClientsSize.value)()
            # Get the connected clients from the LIN hardware.
            linResult = self.m_objPLinApi.GetHardwareParam(
                self.m_hHw, PLinApi.TLIN_HARDWAREPARAM_CONNECTED_CLIENTS, lhClients, lhClientsSize)
            if (linResult == PLinApi.TLIN_ERROR_OK):
                # No errors !
                # Check all client handles.
                for i in range(1, lhClientsSize.value):
                    # If client handle is invalid
                    if (lhClients[i] == 0):
                        continue
                    # Set the boolean to true if the handle isn't the
                    # handle of this application.
                    # Even the boolean is set to true it can never
                    # set to false.
                    lfOtherClient = lfOtherClient | (
                        lhClients[i] != self.m_hClient.value)
                    # Set the boolean to true if the handle is the
                    # handle of this application.
                    # Even the boolean is set to true it can never
                    # set to false.
                    lfOwnClient = lfOwnClient | (
                        lhClients[i] == self.m_hClient.value)
            # If another application is also connected to
            # the LIN hardware do not reset the configuration.
            if (lfOtherClient == False):
                # No other application connected !
                # Reset the configuration of the LIN hardware.
                linResult = self.m_objPLinApi.ResetHardwareConfig(
                    self.m_hClient, self.m_hHw)
            # If this application is connected to the hardware
            # then disconnect the client. Otherwise not.
            if (lfOwnClient == True):
                # Disconnect if the application was connected to a LIN
                # hardware.
                linResult = self.m_objPLinApi.DisconnectClient(
                    self.m_hClient, self.m_hHw)
                if (linResult == PLinApi.TLIN_ERROR_OK):
                    self.m_hHw = PLinApi.HLINHW(0)
                    return True
                else:
                    # Error while disconnecting from hardware.
                    self.showMessageError(linResult)
                    return False
            else:
                return True
        else:
            # m_hHw not connected
            return True


        # Reads PLIN messages
    #
    #收取信息的过程为：首先调用读取函数，读取信息（返回值不能是错误）；然后处理信息；然后在把新收到的
    #信息插入到队列中，再调用显示函数显示出来
    def readMessages(self):
        """
        Reads PLIN messages

        Returns:
            None
        """
        # We read at least one time the queue looking for messages.
        # If a message is found, we look again trying to find more.
        # If the queue is empty or an error occurs, we get out from
        # the do while statement.
        m_LastLINErr = PLinApi.TLIN_ERROR_OK
        # note: using self.btnRelease['state'] is not advised
        # to detect hardware connection as Tk may hold thread execution
        # if GUI operation are made (like moving the window)

        #判断连接是否存在，收到的lin错误
        while (not (self.m_hHw.value == 0) and not (m_LastLINErr & PLinApi.TLIN_ERROR_RCVQUEUE_EMPTY)):
            #结构体
            lpMsg = PLinApi.TLINRcvMsg()

            #判断读取是否成功
            m_LastLINErr = self.m_objPLinApi.Read(self.m_hClient, lpMsg)
            # If at least one Frame is received by the LinApi.
            # Check if the received frame is a standard type.
            # If it is not a standard type than ignore it.
            #不是标准的，则继续收取
            if (lpMsg.Type != PLinApi.TLIN_MSGTYPE_STANDARD.value):
                print('不是标准的lin帧，将重新拾取\n')
                continue
            # process message
            if (m_LastLINErr == PLinApi.TLIN_ERROR_OK):
                print('读取信息成功')
                self.processMessage(lpMsg)
    # Processes a received message, in order to show it in the Message-ListView
    #

    def processMessage(self, linMsg):
        """
        Processes a received message, in order to show it in the Message-ListView.

        Parameters:
            linMsg  a TLINRcvMsg object

        Returns:
            None
        """
        # prevent concurrency errors with timers (read and display)

            # search if a message (Same ID and Type) has
            # already been received or if this is a new message
            #msg 是个类对象
        """
        for msg in self.m_LastMsgsList:
            if (msg.m_Msg.FrameId == linMsg.FrameId):
                    # Modify the message and exit
                msg.update(linMsg)
                return
            # Message not found. It will be created

        """
        self.insertMsgEntry(linMsg)

    # Inserts a new entry for a new message in the Message-ListView
    # Displays and updates LIN messages in the Message-ListView
    #
    def insertMsgEntry(self, newMsg):
        """
        Displays and updates LIN messages in the Message-ListView.

        Parameters:
            newMsg The messasge to be inserted

        Returns:
            None
        """
        # prevent concurrency errors with timers (read and display)
        #with self._lock:
        # #上下文管理器
            # add this status in the last message list

            #MessageStatus 是个类，创立一个类对象msgStsCurrentMsg
        msgStsCurrentMsg = MessageStatus(newMsg, len(self.m_LastMsgsList))

            #m_LastMsgsList 是个列表，把新信息加入列表
        self.m_LastMsgsList.append(msgStsCurrentMsg)

            #test 20210413,调用显示函数
        print(self.formatMsgStatus(msgStsCurrentMsg))

        #lstMessages显示控件，把信息显示出来，通过调用显示函数


    # Formats the object to be displayed in a ListBox
    #以一定的格式来排列收到的信息，显示在框中
    def formatMsgStatus(self, msgStatus):
        """
        Formats the object to be displayed in a ListBox

        Returns:
            the MessageStatus formatted as a string for a listBox
        """

        strTemp = msgStatus.getDataString()

        result = strTemp

        return result

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = mywindow()
    demo.ui.show()
    sys.exit(app.exec_())