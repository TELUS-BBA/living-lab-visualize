import React from 'react';
import Display from './display';
import Login from './login';


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
        { this.state.username &&
          <Display username={this.state.username} password={this.state.password}/>
        }
        { !this.state.username &&
          <Login 
            username={this.state.username}
            password={this.state.password}
            updateCredentials={this.updateCredentials}
          />
        }
      </div>
    );
  }
}

export default TopLevel;
