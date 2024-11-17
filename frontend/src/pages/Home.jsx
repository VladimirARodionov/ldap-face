import React, { useState, useEffect } from 'react';
import Layout from "../components/Layout";
import useSWR from "swr";
import { fetcher } from "../helpers/axios";
import { getUser } from "../hooks/user.actions";
import { Tree } from 'primereact/tree';
import { NodeService } from '../components/NodeService';

function Home() {
  const user = getUser();
    const [nodes, setNodes] = useState([]);
    const [selectedKey, setSelectedKey] = useState('');

    useEffect(() => {
        NodeService.getTreeNodes().then((data) => setNodes(data));
    }, []);

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
