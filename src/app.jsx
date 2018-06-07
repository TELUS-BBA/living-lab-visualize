import React from 'react';
import TopLevel from  './top-level';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: "",
    };
    this.updateCredentials = this.updateCredentials.bind(this);
  }

  updateCredentials(username, password) {
    this.setState({
      username: username,
      password: password,
    });
  }


  render() {
    return (
      <div>
        <TopLevel username={this.state.username} password={this.state.password}/>
      </div>
    );
  }
}

export default App;
