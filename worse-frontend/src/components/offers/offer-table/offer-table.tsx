import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import { Table, Input, Button, Space, Spin } from "antd";
import Highlighter from "react-highlight-words";
import { SearchOutlined } from "@ant-design/icons";
import axios from "axios";
import { Content } from "antd/lib/layout/layout";
import "./offer-table.scss";

export default function OfferTable() {
  const [offers, setOffers] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [searchState, setSearchState] = useState<{
    searchText: any;
    searchedColumn: any;
  }>();
  const [searchInput, setSearchInput] = useState<any>(null);

  // Endpoint for retrieval of the wine offers from after a given timestamp.
  const getOffersURL = "http://localhost:49500/recommendation";

  // Requests the wine offer data from the database.
  const fetchData = async () => {
    setLoading(true);
    const response = await axios.get(getOffersURL, {
      headers: {
        'X-Token': 23984728947
      }
    });
    setOffers(response.data);
    setLoading(false);

    return response.data;
  };

  // A React hook that fetches data when the component is mounted.
  useEffect(() => {
    fetchData();
  }, []);

  // Defines the dropdown elements for the, which recommender algorithm to filter on.
  const DropdownItems = (
    <Menu>
      <Menu.Item key="0" onClick={e => setChosenDropdownItem(0)}>
        Support Vector Machine {chosenDropdownItem === 0? <CheckOutlined /> : <div/>}
      </Menu.Item>
      <Menu.Item key="1" onClick={e => setChosenDropdownItem(1)}>
        Naive Bayes {chosenDropdownItem === 1? <CheckOutlined /> : <div/>}
      </Menu.Item >
      <Menu.Item key="2" onClick={e => setChosenDropdownItem(2)}>
        Logistic Regression {chosenDropdownItem === 2? <CheckOutlined /> : <div/>}
      </Menu.Item>
      <Menu.Divider />
      <Menu.Item key="3" onClick={e => setChosenDropdownItem(3)}>
        Show all offers {chosenDropdownItem === 3? <CheckOutlined /> : <div/>}
      </Menu.Item>
    </Menu>
  );

  // Filters the data for the table depending on the chosen recommender algorithm.
  useEffect(() => {
    if(chosenDropdownItem === 0) {
      setData(offers.filter(x => x.svm_key != null));
    } else if (chosenDropdownItem === 1) {
      setData(offers.filter(x => x.nb_key != null));
    } else if (chosenDropdownItem === 2) {
      setData(offers.filter(x => x.logit_key != null));
    } else {
      setData(offers);
    }
  }, [chosenDropdownItem, offers]);

  const handleDropdownItem = () => {
    if(chosenDropdownItem === 0) {
      return "Support Vector Machine";
    } else if (chosenDropdownItem === 1) {
      return "Naive Bayes";
    } else if (chosenDropdownItem === 2) {
      return "Logistic Regression";
    } else {
      return "Show all offers"
    }
  } 


  // Handles the routing for accessing a particular wine offer page.
  let history = useHistory();
  function handleRowClick(id: string) {
    history.push(`/offers/${id}`);
  }


  // Creates the search functionality on the different columns in the offer table.
  const getColumnSearchProps = (dataIndex: any, key?: any) => ({
    filterDropdown: ({
      setSelectedKeys,
      selectedKeys,
      confirm,
      clearFilters,
    }: any) => (
      <div style={{ padding: 8 }}>
        <Input
          ref={(node) => {
            setSearchInput(node);
          }}
          placeholder={`Search ${key ? key : dataIndex}`}
          value={selectedKeys[0]}
          onChange={(e) =>
            setSelectedKeys(e.target.value ? [e.target.value] : [])
          }
          onPressEnter={() => handleSearch(selectedKeys, confirm, dataIndex)}
          style={{ width: 188, marginBottom: 8, display: "block" }}
        />
        <Space>
          <Button
            type="primary"
            onClick={() => handleSearch(selectedKeys, confirm, dataIndex)}
            icon={<SearchOutlined />}
            size="small"
            style={{ width: 90 }}
          >
            Search
          </Button>
          <Button
            onClick={() => handleReset(clearFilters)}
            size="small"
            style={{ width: 90 }}
          >
            Reset
          </Button>
        </Space>
      </div>
    ),
    filterIcon: (filtered: any) => (
      <SearchOutlined style={{ color: filtered ? "#1890ff" : undefined }} />
    ),
    onFilter: (value: any, record: any) =>
      record[dataIndex]
        ? record[dataIndex]
            .toString()
            .toLowerCase()
            .includes(value.toLowerCase())
        : "",
    onFilterDropdownVisibleChange: (visible: any) => {
      if (visible) {
        setTimeout(() => searchInput?.select(), 100);
      }
    },
    render: (text: string) =>
      searchState?.searchedColumn === dataIndex ? (
        <Highlighter
          highlightStyle={{ backgroundColor: "#ffc069", padding: 0 }}
          searchWords={[searchState?.searchText]}
          autoEscape
          textToHighlight={text ? text.toString() : ""}
        />
      ) : (
        text
      ),
  });

  // Functionality for pressing search button.
  const handleSearch = (selectedKeys: any, confirm: any, dataIndex: any) => {
    confirm();
    setSearchState({
      searchText: selectedKeys[0],
      searchedColumn: dataIndex,
    });
  };

  // Functionality for resetting the searchfield.
  const handleReset = (clearFilters: any) => {
    clearFilters();
    setSearchState({ searchText: "", searchedColumn: "" });
  };


   // Defines the columns for the offer table.
   const offerTableColumns = [
    {
      title: "Id",
      dataIndex: "id",
      key: "id",
      ...getColumnSearchProps("id"),
    },
    {
      title: "Wine Name",
      dataIndex: "wineName",
      key: "wineName",
      width: "50%",
      ...getColumnSearchProps("wineName", "wine name"),
    },
    {
      title: "Year",
      dataIndex: "year",
      key: "year",
      sorter: (a: any, b: any) => a.year - b.year,
      ...getColumnSearchProps("year"),
    },
    {
      title: "Price",
      dataIndex: "price",
      key: "price",
      width: "10%",
      sorter: (a: any, b: any) => a.price - b.price,
    },
    {
      title: "Currency",
      dataIndex: "currency",
      filters: [
        {
          text: "€",
          value: "€",
        },
        {
          text: "$",
          value: "$",
        },
      ],
      key: "currency",
      onFilter: (value: any, record: any) =>
        record.currency.indexOf(value) === 0,
      width: "10%",
    },
  ];

  return (
    <Content style={{ margin: "0 16px" }}>
      <div className="headerText"> Wine Offer Recommendations </div>
      <div
        className="site-layout-background"
        style={{ padding: 24, minHeight: 360 }}
      >
        <Row justify={"end"}>
          <Dropdown overlay={DropdownItems} trigger={['click']} >
            <a className="ant-dropdown-link" onClick={e => e.preventDefault()}>
              {handleDropdownItem()}  <DownOutlined />
            </a>
          </Dropdown>
        </Row>
        <div style={{ height: "30px" }}></div>
        {loading ? (
          <div className="spin">
            <Spin size="large" />
          </div>
        ) : (
          <Table
            columns={offerTableColumns}
            dataSource={offers}
            onRow={(record, rowIndex) => {
              return {
                onClick: (event) => {
                  return handleRowClick(record.id);
                },
              };
            }}
          />
        )}
      </div>
    </Content>
  );
}
