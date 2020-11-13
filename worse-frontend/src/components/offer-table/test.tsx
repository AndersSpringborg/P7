import gql from "graphql-tag";

import { useQuery } from "@apollo/react-hooks";

import getData from "../general/useGetApolloData";

const query = gql`
  query getWineByLwin($wine: String!) {
    GetWine(wine: $wine)
      @rest(type: "GetWine", path: "wine/getWine/{args.wine}", method: "GET") {
      id
      producer
      producerAliases
      wineName
      wineNameAliases
      lwin
      lwinRef
      country
      region
      subRegion
      colour
      type
      classification
      dateAddedToLwin
    }
  }
`;

export default (wineId: string | number | undefined) => {
  const { data, loading, error } = useQuery<ApolloDataWrapper<Wine>>(query, {
    variables: { wine: wineId },
    skip: !wineId,
  });

  return { data: getData(data), loading, error };
};
