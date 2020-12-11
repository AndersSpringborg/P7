import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import { Table, Input, Button, Space, Spin, Dropdown, Menu, Row } from "antd";
import Highlighter from "react-highlight-words";
import { CheckOutlined, DownOutlined, SearchOutlined } from "@ant-design/icons";
import axios from "axios";
import { Content } from "antd/lib/layout/layout";
import "./related-offers-table.scss";

export default function RelatedOffersTable(props: {id: any, LWIN? : any}) {
  const [offers, setOffers] = useState<WineOffer[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [searchState, setSearchState] = useState<{
    searchText: any;
    searchedColumn: any;
  }>();
  const [searchInput, setSearchInput] = useState<any>(null);

  // Endpoint for retrieval of the wine offers from after a given timestamp.
  const getOffersURL = `http://localhost:49500/offersFromLwin/?id=${props.id}&lwin=${props.LWIN || ""}`;

  // Requests the wine offer data from the database.
  const fetchData = async () => {
    setLoading(true);
    const response = await axios.get(getOffersURL);
    setOffers(response.data);
    setLoading(false);

    return response.data;
  };

  // A React hook that fetches data when the component is mounted.
  useEffect(() => {
    fetchData();
  }, []);


  // Handles the routing for accessing a particular wine offer page.
  let history = useHistory();
  function handleRowClick(id: string) {
    history.push(`/offers/${id}`);
    refreshPage();
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


  // Refreshes page.
  const refreshPage = () => {
    window.location.reload(false);
  }


   // Defines the columns for the related offer table.
   const offerTableColumns = [
    {
      title: "LWIN",
      dataIndex: "linkedWineLwin",
      key: "linkedWineLwin",
      sorter: (a: any, b: any) => a.linkedWineLwin - b.linkedWineLwin,
      ...getColumnSearchProps("linkedWineLwin"),
    },
    {
      title: "Wine Name",
      dataIndex: "wineName",
      key: "wineName",
      width: "50%",
      ...getColumnSearchProps("wineName", "wine name"),
    },
    {
      title: "Quantity",
      dataIndex: "quantity",
      key: "quantity",
      sorter: (a: WineOffer, b: WineOffer) => a.quantity - b.quantity,
      ...getColumnSearchProps("quantity"),
    },
    {
      title: "Price",
      dataIndex: "price",
      key: "price",
      width: "10%",
      sorter: (a: WineOffer, b: WineOffer) => a.price - b.price,
      ...getColumnSearchProps("price"),
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
      onFilter: (value: any, record: WineOffer) =>
        record.currency.indexOf(value) === 0,
      width: "10%",
    },
    {
      title: "Price Difference",
      dataIndex: "price_difference",
      key: "price_difference",
      sorter: (a: WineOffer, b: WineOffer) => a.price_difference - b.price_difference,
    },
  ];

  return (
    <Content style={{ margin: "0 16px" }}>
      <div
        className="site-layout-background"
        style={{ padding: 24, minHeight: 360 }}
      >
        <h1 className="header2Text">Other deals for same wine</h1>
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
