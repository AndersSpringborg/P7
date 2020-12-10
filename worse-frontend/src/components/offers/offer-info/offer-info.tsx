import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useHistory } from "react-router-dom";
import { Row, Col, Divider, Spin } from "antd";
import { EnvironmentOutlined, EuroOutlined, ExperimentOutlined, EyeOutlined, FieldNumberOutlined, FieldTimeOutlined, FrownOutlined, GifOutlined, GiftOutlined, GlobalOutlined, GoldOutlined, HourglassOutlined, LeftCircleOutlined, MailOutlined, MessageOutlined, UserOutlined } from "@ant-design/icons";
import axios from "axios";
import { Content } from "antd/lib/layout/layout";
import "./offer-info.scss";

export default function WineInfo() {
  const [wines, setWines] = useState<WineOffer[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const { id }: any = useParams();
  const apiURL = `http://localhost:49500/wine/${id || ""}`;
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    const response = await axios.get(apiURL);

    setWines(response.data);
    setLoading(false);
    return response.data;
  };

  let history = useHistory();

  return (
    <Content style={{ margin: "0 16px" }}>
      <div className="goBack">
        <LeftCircleOutlined className="goBack" onClick={history.goBack} />
      </div>
      {loading ? (
        <div className="spin">
          <Spin size="large" />
        </div>
      ) : (
        <>
          <div className="headerText">
            {" "}
            {wines[0]?.wineName} {wines[0]?.year}{" "}
          </div>
          <div
            //sstyle={{ padding: 24, minHeight: 360 }}
          >
            <Row style={{ justifyContent: "center" }}>
              <Row justify="center" className="infoBox">
                <Col style={{ width: "40vh" }}>
                  <h1 className="header2Text">Offer & Supplier</h1>
                  <Col>
                    <Row>
                      <div className="icon">
                        <EuroOutlined/>
                      </div>
                      <span className="text">
                        Price: {wines[0]?.price} {wines[0]?.currency}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <GoldOutlined/>
                      </div>
                      <span className="text">
                        Quantity: {wines[0]?.quantity}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <UserOutlined/>
                      </div>
                      <span className="text">
                        Name: {wines[0]?.supplierName}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <MailOutlined/>
                      </div>
                      <span className="text">
                        Email: {wines[0]?.supplierEmail}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <MessageOutlined/>
                      </div>
                      <span className="text"> Original offer text: </span>
                      <span className="text" style={{ margin: "10px 0px 0px 50px" }}> {wines[0]?.originalOfferText} </span>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <FieldTimeOutlined/>
                      </div>
                      <span className="text">
                        Created at: {wines[0]?.createdAt}
                      </span>
                    </Row>
                  </Col>
                </Col>
              </Row>
              <div style={{ width: "110px" }}/>
              <Row justify="center" className="infoBox">
                <Col style={{ width: "40vh" }}>
                  <h1 className="header2Text">Wine</h1>
                  <Col>
                    <Row>
                      <div className="icon">
                        <EyeOutlined/>
                      </div>
                      <span className="text">
                        Name: {wines[0]?.wineName}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <UserOutlined/>
                      </div>
                      <div className="text">
                        Producer: {wines[0]?.producer}
                      </div>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <GlobalOutlined/>
                      </div>
                      <span className="text">Region: {wines[0]?.region}</span>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <EnvironmentOutlined/>
                      </div>
                      <span className="text">
                        Sub Region: {wines[0]?.subRegion}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <HourglassOutlined/>
                      </div>
                      <span className="text">Year: {wines[0]?.year}</span>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <ExperimentOutlined/>
                      </div>
                      <span className="text">Colour: {wines[0]?.colour}</span>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <FieldNumberOutlined/>
                      </div>
                      <span className="text">
                        LWIN: {wines[0]?.linkedWineLwin}
                      </span>
                    </Row>
                  </Col>
                </Col>
              </Row>
              <div style={{ width: "110px" }}></div>
              <Row justify="center" className="infoBox">
                <Col style={{ width: "40vh" }}>
                  <h1 className="header2Text">Packaging</h1>
                  <Col>
                    <Row>
                      <div className="icon">
                        <GiftOutlined/>
                      </div>
                      <span className="text">
                        Package Features: {wines[0]?.isOWC} {wines[0]?.isOC}{" "}
                        {wines[0]?.isIB}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <GoldOutlined/>
                      </div>
                      <span className="text">
                        Bottles per case: {wines[0]?.bottlesPerCase}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <ExperimentOutlined/>
                      </div>
                      <span className="text">
                        Bottle size: {wines[0]?.bottleSize}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <div className="icon">
                        <ExperimentOutlined/>
                      </div>
                      <span className="text">
                        Bottle size (numerical): {wines[0]?.bottleSizeNumerical}
                      </span>
                    </Row>
                  </Col>
                </Col>
              </Row>
            </Row>
            <div style={{ height: "60px" }}></div>
          </div>
        </>
      )}
    </Content>
  );
}
