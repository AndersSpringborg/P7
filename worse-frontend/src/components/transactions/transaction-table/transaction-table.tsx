import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import { Table, Input, Button, Space } from "antd";
import Highlighter from "react-highlight-words";
import { SearchOutlined } from "@ant-design/icons";
import axios from "axios";
import { Content } from "antd/lib/layout/layout";

export default function TransactionTable() {
  const [wines, setWines] = useState<any[]>([]);

  const apiURL = "http://localhost:5000/GetAllTransactions";

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const response = await axios.get(apiURL);

    setWines(response.data);
    console.log(response.data);

    return response.data;
  };

  let history = useHistory();

  function handleRowClick(id: string) {
    history.push(`/wineOffer/${id}`);
  }

  const state = {
    searchText: "",
    searchedColumn: "",
  };

  const [searchState, setSearchState] = useState<{
    searchText: any;
    searchedColumn: any;
  }>();
  const [searchInput, setSearchInput] = useState<any>(null);

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
          searchWords={[state.searchText]}
          autoEscape
          textToHighlight={text ? text.toString() : ""}
        />
      ) : (
        text
      ),
  });

  const handleSearch = (selectedKeys: any, confirm: any, dataIndex: any) => {
    confirm();
    setSearchState({
      searchText: selectedKeys[0],
      searchedColumn: dataIndex,
    });
  };

  const handleReset = (clearFilters: any) => {
    clearFilters();
    setSearchState({ searchText: "", searchedColumn: "" });
  };

  const columns = [
    {
      title: "Vendor Id",
      dataIndex: "vendorId",
      key: "vendorId",
      ...getColumnSearchProps("vendorId", "vendor id"),
    },
    {
      title: "Description",
      dataIndex: "description",
      key: "description",
      width: "50%",
      ...getColumnSearchProps("description"),
    },
    {
      title: "LWIN",
      dataIndex: "lwinnumber",
      key: "lwinnumber",
      sorter: (a: any, b: any) => a.lwinnumber - b.lwinnumber,
      ...getColumnSearchProps("lwinnumber"),
    },
    {
      title: "Price",
      dataIndex: "amount",
      key: "amount",
      width: "10%",
      sorter: (a: any, b: any) => a.amount - b.amount,
      ...getColumnSearchProps("amount"),
    },
  ];

  return (
    <Content style={{ margin: "0 16px" }}>
      <div className="headerText"> Previous Transactions </div>
      <div
        className="site-layout-background"
        style={{ padding: 24, minHeight: 360 }}
      >
        <Table
          columns={columns}
          dataSource={wines}
          onRow={(record, rowIndex) => {
            return {
              onClick: (event) => {
                return handleRowClick(record.id);
              }
            };
          }}
        />
      </div>
    </Content>
  );
}
