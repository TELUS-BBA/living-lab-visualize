import React from 'react';
import FlexGrid from '@tds/core-flex-grid';
import HairlineDivider from '@tds/core-hairline-divider';

import Login from './login';
import Filter from './filter';
import Graph from './graph';


class TopLevel extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: "",
    };
    this.updateCredentials = this.updateCredentials.bind(this);
  }

  updateCredentials(username, password) {
    console.log(`${this.state.username} ${this.state.password}`);
    this.setState({
      username: username,
      password: password,
    });
  }

  render() {
    return (
      <div>
        <Login 
          username={this.state.username}
          password={this.state.password}
          updateCredentials={this.updateCredentials}
        />
        <HairlineDivider />
        <FlexGrid>
          <FlexGrid.Row>
            <FlexGrid.Col lg={3}>
              <Filter
              />
            </FlexGrid.Col>
            <FlexGrid.Col>
              <HairlineDivider vertical />
            </FlexGrid.Col>
            <FlexGrid.Col lg={9}>
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

export default TopLevel;
