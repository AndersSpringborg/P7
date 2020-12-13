import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useHistory } from "react-router-dom";
import { Row, Col, Divider, Spin } from "antd";
import { LeftCircleOutlined } from "@ant-design/icons";
import axios from "axios";
import { Content } from "antd/lib/layout/layout";
import "./transaction-info.scss";

export default function TransactionInfo() {
  const [transaction, setTransaction] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const { id }: any = useParams();
  const apiURL = `http://localhost:49500/transaction/${id || ""}`;
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    const response = await axios.get(apiURL);

    setTransaction(response.data);
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
            {transaction[0]?.description}{" "}
          </div>
          <div
            //sstyle={{ padding: 24, minHeight: 360 }}
          >
            <Row style={{ justifyContent: "center" }}>
              <Row justify="center" className="infoBox">
                <Col style={{ width: "40vh" }}>
                  <h1 className="header2Text">Information</h1>
                  <Col>
                    <Row>
                      <span className="text">
                        VendorId: {transaction[0]?.vendorId}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <span className="text">
                        PostingGroup: {transaction[0]?.postingGroup}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <span className="text">
                        Number: {transaction[0]?.number}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <span className="text">
                        LWIN: {transaction[0]?.lwinNumber}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <span className="text">
                        Description: {transaction[0]?.description}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <span className="text">
                        Measurement Unit: {transaction[0]?.measurementunit}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <span className="text">
                        Quantity: {transaction[0]?.quantity}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <span className="text">
                        Direct Unit Cost: {transaction[0]?.directunitcost}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <span className="text">
                        Amount: {transaction[0]?.amount}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <span className="text">
                        Variant Code: {transaction[0]?.variantcode}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <span className="text">
                        Posting Date: {transaction[0]?.postingdate}
                      </span>
                    </Row>
                    <Divider />
                    <Row>
                      <span className="text">
                        Offer ID: {transaction[0]?.offers_FK}
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