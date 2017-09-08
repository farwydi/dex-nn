class Neuron
{
  public:
    Neuron();
    ~Neuron();

    float getDelta(void) const { return delta; }
    float getPower(void) const { return power; }

  private:
    float delta;
    float power;
};

class Connect
{
  public:
    Connect(Neuron *_base, Neuron *_way)
        : base(_base), way(_way)
    {
        deltaWeight = 0;
    }

    ~Connect();

    float echo(void)
    {
        return way->getPower() * weight;
    }

    void learning(float E, float A)
    {
        float gradWeight = base->getDelta() * way->getPower();

        deltaWeight = (E * gradWeight) + (A * deltaWeight);
        weight = weight + deltaWeight;
    }

  private:
    float weight;
    float deltaWeight;
    
    Neuron *base;
    Neuron *way;
};
