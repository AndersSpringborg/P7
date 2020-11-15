import React, { useState } from "react";
import "./worst-layout.scss";
import { Layout, Menu, Image, Switch } from "antd";
import { UnorderedListOutlined } from "@ant-design/icons";
import juleLogo from "./../images/worstlogo1.png";
import logo from "./../images/worstlogo.png";
import christmaslights from "./../images/christmaslight.png";
import { useHistory } from "react-router-dom";

const { Header, Footer, Sider } = Layout;

export default function WorstLayout (props: any) {
  const [collapsed, setCollapsed] = useState<boolean>(false);
  const [juled, setJuled] = useState<boolean>(false);

  const onCollapse = () => {
    collapsed? (setCollapsed(false)) : (setCollapsed(true));
  };

  const onJule = () => {
    juled? (setJuled(false)) : (setJuled(true));
  };

  let history = useHistory();

  const handleTransactionClick = () => {
    history.push(`/transactions`);
  }

  const handleOfferClick = () => {
    history.push(`/`);
  }

    return (
      <Layout style={{ minHeight: "100vh" }}>
        <Sider collapsible collapsed={collapsed} onCollapse={onCollapse}>
          <div className="logo">
            {juled ? (
              <Image className="juleimg" src={juleLogo} alt="ant image" />
            ) : (
              <Image className="juleimg" src={logo} alt="ant image" />
            )}
          </div>
          <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline">
            <Menu.Item key="1" icon={<UnorderedListOutlined />} onClick={handleOfferClick}>
              Offers
            </Menu.Item>
            <Menu.Item key="2" icon={<UnorderedListOutlined />} onClick={handleTransactionClick}>
              Transactions
            </Menu.Item>
          </Menu>
          <Switch className="juleKnap" onChange={onJule} />
        </Sider>
        <Layout className="site-layout">
          <Header className="site-layout-background" style={{ padding: 0 }}>
            {juled ? (
              <Image
                className="juleimg"
                src={christmaslights}
                alt="ant image"
              />
            ) : (
              <div />
            )}
          </Header>
          <div>
          { props.children  }
          </div>
          <Footer style={{ textAlign: "center" }}>
            WORST (Wine Offer Recommender System for Traders) 2020©
          </Footer>
        </Layout>
      </Layout>
    );

}
