import React, {Component} from 'react';
import TopAppBar, {
    TopAppBarFixedAdjust,
    TopAppBarIcon,
    TopAppBarRow,
    TopAppBarSection,
    TopAppBarTitle
} from '@material/react-top-app-bar';
import Drawer, {DrawerAppContent, DrawerContent, DrawerHeader, DrawerTitle,} from '@material/react-drawer';
import MaterialIcon from '@material/react-material-icon';
import List, {ListItem, ListItemGraphic, ListItemMeta, ListItemText} from '@material/react-list';
import Button from '@material/react-button';
import ReconnectingWebSocket from './reconnecting-websocket';
import Conversation from './Conversation';

import './App.scss';

const SockContext = React.createContext(null);

class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            open: true,
            lastMessage: 0,
            selectedIndex: null,
            conversations: [],
            conversationMap: {}
        };

        this.selectConversation = this.selectConversation.bind(this);
        this.handleOpen = this.handleOpen.bind(this);
        this.handleReceiveMessage = this.handleReceiveMessage.bind(this);
        this.onSend = this.onSend.bind(this);
        this.onEnd = this.onEnd.bind(this);
        this.onFinish = this.onFinish.bind(this);
    }

    componentDidMount() {
        this.sock = new ReconnectingWebSocket(process.env.NODE_ENV === 'production' ?
            "wss://" + window.location.host + "/ws/operator/" : "ws://localhost:8000/ws/operator/", null, {automaticOpen: false});
        this.sock.onopen = this.handleOpen;
        this.sock.onmessage = this.handleReceiveMessage;
        this.sock.open();
    }

    componentWillUnmount() {
        this.sock.close();
    }

    selectConversation(i) {
        this.setState({
            selectedIndex: i
        })
    }

    handleReceiveMessage(msg) {
        const data = JSON.parse(msg.data);

        const message = {
            id: data.id,
            direction: data.direction,
            timestamp: data.timestamp,
            text: data.text,
            image: data.image,
            read: data.read,
        };
        const conversations = this.state.conversations;
        const conversationMap = this.state.conversationMap;
        let conversationId = conversationMap[data.conversation.id];
        let conversation = {
            customer_name: data.conversation.customer_name,
            username: data.conversation.customer_username,
            picture: data.conversation.customer_pic,
            agent_responding: data.conversation.agent_responding,
            timezone: data.conversation.timezone,
            customer_email: data.conversation.customer_email,
            customer_phone: data.conversation.customer_phone,
            payments: data.conversation.payments
        };
        if (typeof conversationId === "undefined") {
            conversationId = conversations.push(Object.assign({
                id: data.conversation.id,
                messages: [message],
                messageMap: {}
            }, conversation)) - 1;
            conversationMap[data.conversation.id] = conversationId;
        } else {
            let oldConversation = conversations[conversationId];
            conversations[conversationId] = Object.assign(oldConversation, conversation);
        }
        let messageId = conversations[conversationId].messageMap[data.id];
        if (typeof messageId === "undefined") {
            messageId = conversations[conversationId].messages.push(message) - 1;
            conversations[conversationId].messageMap[data.id] = messageId;
        } else {
            let oldMessage = conversations[conversationId].messages[messageId];
            conversations[conversationId].messages[messageId] = Object.assign(oldMessage, message)
        }
        this.setState({
            conversations: conversations,
            conversationMap: conversationMap,
            lastMessage: message.timestamp,
        });
    }

    handleOpen() {
        this.sock.send(JSON.stringify({
            "type": "resyncReq",
            "lastMessage": this.state.lastMessage
        }));
    }

    onSend(text) {
        this.sock.send(JSON.stringify({
            "type": "msg",
            "text": text,
            "cid": this.state.conversations[this.state.selectedIndex].id
        }));
    }

    onEnd() {
        this.sock.send(JSON.stringify({
            "type": "endConv",
            "cid": this.state.conversations[this.state.selectedIndex].id
        }));
    }

    onFinish() {
        this.sock.send(JSON.stringify({
            "type": "finishConv",
            "cid": this.state.conversations[this.state.selectedIndex].id
        }));
        const conversations = this.state.conversations;
        conversations[this.state.selectedIndex].agent_responding = true;
        this.setState({
            conversations: conversations
        })
    }

    render() {
        return (
            <div className='drawer-container'>
                <Drawer dismissible open={this.state.open}>
                    <DrawerHeader>
                        <DrawerTitle tag='h2'>
                            Agent interface
                        </DrawerTitle>
                    </DrawerHeader>

                    <DrawerContent>
                        <List twoLine avatarList singleSelection selectedIndex={this.state.selectedIndex}>
                            {this.state.conversations
                                .map((c, i) => {
                                    return {c: c, i: i, lastMsg: c.messages[c.messages.length - 1]}
                                })
                                .sort((f, s) => s.lastMsg.timestamp - f.lastMsg.timestamp)
                                .map(c => (
                                    <ListItem key={c.i} onClick={() => this.selectConversation(c.i)}>
                                        <ListItemGraphic graphic={<img src={c.c.picture} alt=""/>}/>
                                        <ListItemText
                                            primaryText={c.c.customer_name}
                                            secondaryText={c.lastMsg.text}/>
                                        {!c.c.agent_responding ?
                                            <ListItemMeta meta={<MaterialIcon icon='notification_important'/>}/> : null}
                                    </ListItem>
                                ))}
                        </List>
                    </DrawerContent>
                </Drawer>

                <DrawerAppContent className='drawer-app-content'>
                    <TopAppBar>
                        <TopAppBarRow>
                            <TopAppBarSection align='start'>
                                <TopAppBarIcon navIcon>
                                    <MaterialIcon icon='menu' onClick={() => this.setState({open: !this.state.open})}/>
                                </TopAppBarIcon>
                                <TopAppBarTitle>{this.state.selectedIndex === null ? "Loading..." :
                                    this.state.conversations[this.state.selectedIndex].customer_name}</TopAppBarTitle>
                            </TopAppBarSection>
                            <TopAppBarSection role='toolbar'>
                                {this.state.selectedIndex === null ? null :
                                    <React.Fragment>
                                        <Button raised onClick={this.onEnd}>
                                            End conversation
                                        </Button>
                                        <Button raised onClick={this.onFinish}>
                                            Hand back to agent
                                        </Button>
                                    </React.Fragment>
                                }
                            </TopAppBarSection>
                        </TopAppBarRow>
                    </TopAppBar>

                    <TopAppBarFixedAdjust>
                        {this.state.selectedIndex === null ?
                            <h2>Please select a conversation from the drawer</h2> :
                            <SockContext.Provider value={this.sock}>
                                <Conversation
                                    conversation={this.state.conversations[this.state.selectedIndex]}
                                    onSend={this.onSend}
                                />
                            </SockContext.Provider>}
                    </TopAppBarFixedAdjust>
                </DrawerAppContent>
            </div>
        );
    }
}

export default App;
