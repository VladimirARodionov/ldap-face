import React from "react";
import Layout from "../components/Layout";
import { Row, Col } from "react-bootstrap";
import useSWR from "swr";
import { fetcher } from "../helpers/axios";
import { getUser } from "../hooks/user.actions";

function Home() {
  const user = getUser();

  if (!user) {
    return <div>Loading!</div>;
  }

  return (
    <Layout>
      <Row className="justify-content-evenly">
        <Col sm={7}>
          <Row className="border rounded  align-items-center">
          </Row>
        </Col>
      </Row>
    </Layout>
  );
}

export default Home;
