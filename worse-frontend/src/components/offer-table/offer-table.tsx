import React, { useEffect, useState } from "react";
import { Table, Input, Button, Space } from "antd";
import Highlighter from "react-highlight-words";
import { SearchOutlined } from "@ant-design/icons";
import axios from "axios";

export default function OfferTable() {
  const [wines, setWines] = useState<any[]>([]);

  const apiURL = "http://localhost:5000/GetWinesFromTimestamp/2018";

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const response = await axios.get(apiURL);

    setWines(response.data);
    console.log(response.data);

    return response.data;
  };

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
      onFilter: (value: any, record: any) =>
        record.currency.indexOf(value) === 0,
      width: "10%",
    },
  ];

  return <Table columns={columns} dataSource={wines} />;
}
