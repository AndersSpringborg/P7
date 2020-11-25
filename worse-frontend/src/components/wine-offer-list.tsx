import React, { Component } from "react";
import "./wine-offer-list.scss";
import { Layout, Menu, Image } from "antd";
import { UnorderedListOutlined } from "@ant-design/icons";
import OfferTable from "./offer-table/offer-table";
import logo from "./../images/worstlogo.png";

const { Header, Content, Footer, Sider } = Layout;

export default class WineOfferList extends Component {
  state = {
    collapsed: false,
  };

  onCollapse = (collapsed: any) => {
    this.setState({ collapsed });
  };

  render() {
    const { collapsed } = this.state;
    return (
      <Layout style={{ minHeight: "100vh" }}>
        <Sider collapsible collapsed={collapsed} onCollapse={this.onCollapse}>
          <div className="logo">
            <Image src={logo} alt="ant image" />
          </div>
          <Menu theme="dark" mode="inline">
            <Menu.Item key="1" icon={<UnorderedListOutlined />}>
              Recommendations
            </Menu.Item>
          </Menu>
        </Sider>
        <Layout className="site-layout">
          <Header className="site-layout-background" style={{ padding: 0 }} />
          <Content style={{ margin: "0 16px" }}>
            <div className="headerText"> Recommendations </div>
            <div
              className="site-layout-background"
              style={{ padding: 24, minHeight: 360 }}
            >
              <OfferTable />
            </div>
          </Content>
          <Footer style={{ textAlign: "center" }}>
            WORST (Wine Offer Recommender System for Traders) 2020©
          </Footer>
        </Layout>
      </Layout>
    );
  }
}
