import React, {Component} from 'react';
import Tab from '@material/react-tab';
import TabBar from '@material/react-tab-bar';
import List, {ListItem, ListItemText} from '@material/react-list';
import Card from '@material/react-card';
import dateformat from "dateformat";
import OrderCard from "./OrderCard";
import RepairCard from "./RepairCard";
import Dialog, {DialogButton, DialogContent, DialogFooter, DialogTitle} from "@material/react-dialog";
import {entity_map} from "./Conversation";
import TextField, {Input} from "@material/react-text-field";
import MaterialIcon from "@material/react-material-icon";
import Button from "@material/react-button";

export default class CustomerPanel extends Component {
    constructor(props) {
        super(props);

        this.state = {
            activeTab: 0,
            attribute: null,
            attributeValue: "",
        };

        this.updateAttribute = this.updateAttribute.bind(this);
    }


    updateAttribute(choice) {
        if (choice === "confirm") {
            this.props.conversation.save_entity({
                entity: this.state.attribute,
                value: JSON.stringify({
                    value: this.state.attributeValue
                })
            });
        }
        this.setState({attribute: null, attributeValue: ""});
    }

    render() {
        let orderStates = {
            "OPEN": "Open",
            "PAID": "Paid",
            "COMPLETE": "Complete",
        };

        return <React.Fragment>
            <Dialog
                onClose={this.updateAttribute}
                open={!!this.state.attribute}>
                <DialogTitle>Update {entity_map[this.state.attribute]}</DialogTitle>
                <DialogContent>
                    <TextField fullWidth outlined>
                        <Input value={this.state.attributeValue}
                               onChange={(e) => this.setState({attributeValue: e.currentTarget.value})}/>
                    </TextField>
                    <br/>
                    <b>
                        Note: please be certain this is the real data of the customer, the system may also
                        request further authentication from the customer automatically
                    </b>
                </DialogContent>
                <DialogFooter>
                    <DialogButton action='dismiss'>Cancel</DialogButton>
                    <DialogButton action='confirm' isDefault disabled={!this.state.attributeValue.length}>
                        Ok
                    </DialogButton>
                </DialogFooter>
            </Dialog>
            <img src={this.props.conversation.customer_pic} alt="" className="profile"/>
            <TabBar
                activeIndex={this.state.activeTab}
                handleActiveIndexUpdate={i => this.setState({activeTab: i})}
            >
                <Tab>
                    <span className='mdc-tab__text-label'>Info</span>
                </Tab>
                <Tab>
                    <span className='mdc-tab__text-label'>Repairs</span>
                </Tab>
                <Tab>
                    <span className='mdc-tab__text-label'>Ordering</span>
                </Tab>
            </TabBar>
            {this.state.activeTab === 0 ?
                <div className="custInfo">
                    <span>First name:</span>
                    <span>{this.props.conversation.customer_first_name ? this.props.conversation.customer_first_name : "N/A"}</span>
                    <span>
                        <MaterialIcon role="button" icon="edit" onClick={() => this.setState({
                            attribute: "first-name",
                            attributeValue: this.props.conversation.customer_first_name ? this.props.conversation.customer_first_name : ""
                        })}/>
                    </span>
                    <span>Last name:</span>
                    <span>{this.props.conversation.customer_last_name ? this.props.conversation.customer_last_name : "N/A"}</span>
                    <span>
                        <MaterialIcon role="button" icon="edit" onClick={() => this.setState({
                            attribute: "last-name",
                            attributeValue: this.props.conversation.customer_last_name ? this.props.conversation.customer_last_name : ""
                        })}/>
                    </span>
                    <span>Username:</span>
                    <span>{this.props.conversation.customer_username ? this.props.conversation.customer_username : "N/A"}</span>
                    <span/>
                    <span>Bot responding:</span>
                    <span>{this.props.conversation.agent_responding ? "Yes" : "No"}</span>
                    <span/>
                    <span>Timezone:</span>
                    <span>{this.props.conversation.timezone ? this.props.conversation.timezone : "N/A"}</span>
                    <span/>
                    <span>Email:</span>
                    <span>{this.props.conversation.customer_email ? this.props.conversation.customer_email : "N/A"}</span>
                    <span>
                        <MaterialIcon role="button" icon="edit" onClick={() => this.setState({
                            attribute: "email",
                            attributeValue: this.props.conversation.customer_email ? this.props.conversation.customer_email : ""
                        })}/>
                    </span>
                    <span>Phone:</span>
                    <span>{this.props.conversation.customer_phone ? this.props.conversation.customer_phone : "N/A"}</span>
                    <span>
                        <MaterialIcon role="button" icon="edit" onClick={() => this.setState({
                            attribute: "phone-number",
                            attributeValue: this.props.conversation.customer_phone ? this.props.conversation.customer_phone : ""
                        })}/>
                    </span>
                    <span>Locale:</span>
                    <span>{this.props.conversation.customer_locale ? this.props.conversation.customer_locale : "N/A"}</span>
                    <span/>
                    <span>Gender:</span>
                    <span>{this.props.conversation.customer_gender ? this.props.conversation.customer_gender : "N/A"}</span>
                    <span/>
                </div> : null
            }
            {this.state.activeTab === 1 ?
                <div className="repairs">
                    <h3>Search for a repair</h3>
                    <RepairCard conversation={this.props.conversation}/>
                    <h3>Bookings</h3>
                    {this.props.conversation.bookings.map(b => {
                        return <Card key={b.id} outlined className="repair">
                            <h4>{b.time ? dateformat(b.time, "h:MMTT dS mmm yyyy") : null}</h4>
                            {b.repair ? <React.Fragment>
                                <span><b>Brand:</b> {b.repair.device.brand.display_name}</span><br/>
                                <span><b>Device:</b> {b.repair.device.display_name}</span><br/>
                                <span><b>Repair:</b> {b.repair.repair.display_name}</span>
                                <span><b>Price:</b> {b.repair.price}</span><br/>
                                <span><b>Time:</b> {b.repair.time}</span>
                            </React.Fragment> : null }
                        </Card>;
                    })}
                    {this.props.conversation.customer_id ?
                        <React.Fragment>
                            <h3>CLS</h3>
                            <Button ripple colored raised href={`https://cardifftec.uk/customers/customer/${this.props.conversation.customer_id}/`} target="_blank">
                                View customer
                            </Button>
                            <Button ripple colored raised href={`https://cardifftec.uk/tickets/new/${this.props.conversation.customer_id}/`} target="_blank">
                                New ticket
                            </Button>
                        </React.Fragment> : null}
                </div>
                : null}
            {this.state.activeTab === 2 ?
                <div className="ordering">
                    <h3>Current order</h3>
                    <OrderCard conversation={this.props.conversation}/>
                    <h3>Order History</h3>
                    <div className="orderHistory">
                        {this.props.conversation.payments
                            .sort((x, y) => y.timestamp - x.timestamp).map(p => {
                                let d = new Date(0);
                                d.setUTCSeconds(p.timestamp);

                                return <Card key={p.id} className="order" outlined>
                                    <div>{p.id}</div>
                                    <span>State:</span>
                                    <span>{orderStates[p.state]}</span>
                                    <span>Time:</span>
                                    <span>{dateformat(d, "h:MM TT ddd mmm dS yyyy")}</span>
                                    <span>Payment method:</span>
                                    <span>{p.payment_method}</span>
                                    <span>Total:</span>
                                    <span>{p.total} GBP</span>
                                    <div className="items">
                                        <h4>Items</h4>
                                        <List twoLine>
                                            {p.items.map(i => {
                                                return <ListItem key={i.id}>
                                                    <ListItemText primaryText={i.title}
                                                                  secondaryText={`${i.quantity} @ ${i.price} GBP`}/>
                                                </ListItem>
                                            })}
                                        </List>
                                    </div>
                                </Card>
                            })}
                    </div>
                </div> : null
            }

        </React.Fragment>
    }
}