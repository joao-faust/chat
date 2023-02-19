class Participant {
  public static add(participants: string[], nickname: string) {
    const index = participants.indexOf(nickname);
    index === -1 ? participants.push(nickname) : '';
  }

  public static remove(participants: string[], nickname: string) {
    const index = participants.indexOf(nickname);
    index !== -1 ? participants.splice(index, 1) : '';
  }
}

export default Participant;
