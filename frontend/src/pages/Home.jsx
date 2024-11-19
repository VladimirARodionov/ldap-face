import React, { useState } from 'react';
import Layout from "../components/Layout";
import useSWR from "swr";
import { fetcher } from "../helpers/axios";
import { getUser } from "../hooks/user.actions";
import { Tree } from 'primereact/tree';

function Home() {
  const user = getUser();
  const [nodes, setNodes] = useState([]);
  const [selectedKey, setSelectedKey] = useState('');
  const myfetcher = async (url: string) => {
      const response = await fetcher(url);
      setNodes(response.data)
      };
  useSWR("/ldap/", myfetcher);

  if (!user) {
    return <div>Loading!</div>;
  }

  return (
    <Layout>
      <Tree value={nodes} selectionMode="single" selectionKeys={selectedKey}
                              onSelectionChange={(e) => setSelectedKey(e.value)}
                              className="w-full md:w-30rem" />
    </Layout>
  );
}

export default Home;
