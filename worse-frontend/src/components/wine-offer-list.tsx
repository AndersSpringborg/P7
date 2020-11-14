import React, { Component } from "react";
import "./wine-offer-list.scss";
import { Layout, Menu, Image, Switch } from "antd";
import { UnorderedListOutlined } from "@ant-design/icons";
import juleLogo from "./../images/worstlogo1.png";
import logo from "./../images/worstlogo.png";
import christmaslights from "./../images/christmaslight.png";

const { Header, Footer, Sider } = Layout;

export default class WineOfferList extends Component {
  state = {
    collapsed: false,
    juled: false,
  };

  onCollapse = (collapsed: any) => {
    this.setState({ collapsed });
  };

  onJule = (juled: any) => {
    this.setState({ juled });
  };

  render() {
    const { collapsed } = this.state;

    return (
      <Layout style={{ minHeight: "100vh" }}>
        <Sider collapsible collapsed={collapsed} onCollapse={this.onCollapse}>
          <div className="logo">
            {this.state.juled ? (
              <Image className="juleimg" src={juleLogo} alt="ant image" />
            ) : (
              <Image className="juleimg" src={logo} alt="ant image" />
            )}
          </div>
          <Menu
            theme="dark"
            mode="inline"
            style={{ backgroundColor: "#400000" }}
          >
            <Menu.Item
              className="menuItem"
              key="1"
              icon={<UnorderedListOutlined />}
            >
              Recommendations
            </Menu.Item>
          </Menu>
          <Switch className="juleKnap" onChange={this.onJule} />
        </Sider>
        <Layout className="site-layout">
          <Header className="site-layout-background" style={{ padding: 0 }}>
            {this.state.juled ? (
              <Image
                className="juleimg"
                src={christmaslights}
                alt="ant image"
              />
            ) : (
              <div />
            )}
          </Header>
          {this.props.children}
          <Footer style={{ textAlign: "center" }}>
            WORST (Wine Offer Recommender System for Traders) 2020©
          </Footer>
        </Layout>
      </Layout>
    );
  }
}
