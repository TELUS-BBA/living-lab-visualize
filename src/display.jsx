import React from 'react';
import axios from 'axios';
import FlexGrid from '@tds/core-flex-grid';

import Filter from './filter';
import Graph from './graph';


class Display extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      data: [],
    };
    axios.get(
      'http://localhost:5001/nanopi/',
      {auth: {username: this.props.username, password: this.props.password}}
    )
      .then( response => {
        this.setState({data: response.data});
      })
      .catch( error => {
        console.log(error);
      });
  }

  fetchData() {
    console.log("fetching data");
  }

  render() {
    return (
      <div>
        <FlexGrid>
          <FlexGrid.Row>
            <FlexGrid.Col lg={4}>
              <Filter
              />
            </FlexGrid.Col>
            <FlexGrid.Col lg={8}>
              { this.state.data &&
                <Graph
                  data={this.state.data}
                />
              }
            </FlexGrid.Col>
          </FlexGrid.Row>
        </FlexGrid>
      </div>
    );
  }
}

export default Display;
