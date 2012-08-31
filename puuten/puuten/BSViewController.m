//
//  BSViewController.m
//  puuten
//
//  Created by wang jialei on 12-8-5.
//
//

#import "BSViewController.h"
#import "ASIFormDataRequest.h"
#import "Constance.h"
#import "ImageViewCell.h"
#import "WBViewController.h"
#import "BSHeader.h"

@interface BSViewController ()

@end

@implementation BSViewController
@synthesize name=_name;
@synthesize tags=_tags;
@synthesize introduction = _introduction;
@synthesize selfButton;
@synthesize othersButton;
@synthesize bs_id;
@synthesize avatar = _avatar;

- (void)setName:(UILabel *)name{
    _name = name;
}

- (void)setTags:(UITextView *)tags{
    _tags = tags;
}

- (void)setIntroduction:(UITextView *)introduction{
    _introduction = introduction;
}

- (void)setAvatar:(UIImageView *)avatar{
    _avatar = avatar;
}

- (void)didReceiveMemoryWarning
{
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc that aren't in use.
}

- (void)loadInternetData{
    NSString *wb_url_string = [NSString stringWithFormat:@"/business/bs_weibo_list/%d/", bs_id];
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSURL *bsURL = [NSURL URLWithString:wb_url_string relativeToURL:nsURL];
    ASIFormDataRequest *_request=[ASIFormDataRequest requestWithURL:bsURL];
    __weak ASIFormDataRequest *request = _request;
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request setCompletionBlock:^{
        NSData *responseData = [request responseData];
        NSError* error;
        NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        [arrayData addObject:[json objectForKey:@"self"]];
        [arrayData addObject:[json objectForKey:@"others"]];
        _name.text = [json objectForKey:@"name"];
        _tags.text = [json objectForKey:@"tags"];
        _introduction.text = [json objectForKey:@"introduction"];
        NSURL *imageURL = [NSURL URLWithString:[json objectForKey:@"avatar_url"]];
        NSData* data = [[NSData alloc] initWithContentsOfURL:imageURL];
        _avatar.image = [UIImage imageWithData:data];
        [self dataSourceDidLoad];
    }];
    [request setFailedBlock:^{
        [self dataSourceDidError];
    }];
    
    [request startAsynchronous];
}

- (void)dataSourceDidLoad {
    [waterFlow_self reloadData];
    [waterFlow_others reloadData];
}

- (void)dataSourceDidError {
    [waterFlow_self reloadData];
    [waterFlow_others reloadData];
}

#pragma mark WaterFlowViewDataSource
- (NSInteger)numberOfColumsInWaterFlowView:(WaterFlowView *)waterFlowView{
    return 2;
}

- (NSInteger)numberOfAllWaterFlowView:(WaterFlowView *)waterFlowView{
    if([arrayData count])
        return [[arrayData objectAtIndex:waterFlowView.tag] count];
    else
        return 0;
    
}

- (UIView *)waterFlowView:(WaterFlowView *)waterFlowView cellForRowAtIndexPath:(IndexPath *)indexPath{
    
    ImageViewCell *view = [[ImageViewCell alloc] initWithIdentifier:nil];
    
    return view;
}


-(void)waterFlowView:(WaterFlowView *)waterFlowView  relayoutCellSubview:(UIView *)view withIndexPath:(IndexPath *)indexPath{
    
    //arrIndex是某个数据在总数组中的索引
    int arrIndex = indexPath.row * waterFlowView.columnCount + indexPath.column;
    
    NSDictionary *object = [[arrayData objectAtIndex:waterFlowView.tag] objectAtIndex:arrIndex];
    NSURL *nsURL = [[NSURL alloc] initWithString:[object objectForKey:@"thumbnail_pic"]];
    int wb_id = [[object objectForKey:@"wb_id"] intValue];
    ImageViewCell *imageViewCell = (ImageViewCell *)view;
    imageViewCell.indexPath = indexPath;
    imageViewCell.columnCount = waterFlowView.columnCount;
    imageViewCell.tt=1;
    [imageViewCell relayoutViews];
    [(ImageViewCell *)view setImageWithURL:nsURL withWB_ID:wb_id withBS:@"mmmm" withType:0 withDelegate:self];
}


#pragma mark WaterFlowViewDelegate
- (CGFloat)waterFlowView:(WaterFlowView *)waterFlowView heightForRowAtIndexPath:(IndexPath *)indexPath{
    
    int arrIndex = indexPath.row * waterFlowView.columnCount + indexPath.column;
    //NSMutableArray *test = [testData objectAtIndex:waterFlowView.tag];
    NSDictionary *dict = [[arrayData objectAtIndex:waterFlowView.tag] objectAtIndex:arrIndex];
    float height_width_ratio = [[dict objectForKey:@"ratio"] floatValue];
    return waterFlowView.cellWidth*height_width_ratio;
}

- (void)waterFlowView:(WaterFlowView *)waterFlowView didSelectRowAtIndexPath:(IndexPath *)indexPath{
    
    NSLog(@"indexpath row == %d,column == %d",indexPath.row,indexPath.column);
}

- (IBAction)click1:(id)sender {
    waterFlow_self.frame = CGRectMake(0, 115, 320, 460-44-115);
    waterFlow_others.frame = CGRectZero;
}


- (IBAction)click2:(id)sender {
    waterFlow_others.frame = CGRectMake(0, 115, 320, 460-44-115);
    waterFlow_self.frame = CGRectZero;
}

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    _name.text = [NSString stringWithFormat:@"%d", bs_id];
    [super viewDidLoad];
	// Do any additional setup after loading the view.
}

- (void)viewDidAppear:(BOOL)animated
{
    selfButton.frame = CGRectMake(0, 90, 160, 25);
    selfButton.titleLabel.frame = CGRectMake(0, 90, 160, 25);
    [selfButton setTitle:@"商家展示" forState:UIControlStateNormal];
    selfButton.titleLabel.font = [UIFont boldSystemFontOfSize:12];
    othersButton.frame = CGRectMake(160, 90, 160, 25);
    othersButton.titleLabel.frame = CGRectMake(160, 90, 160, 25);
    [othersButton setTitle:@"个人痕迹" forState:UIControlStateNormal];
    othersButton.titleLabel.font = [UIFont boldSystemFontOfSize:12];
    arrayData = [[NSMutableArray alloc] initWithCapacity:2];
    for (int i=0; i<[arrayData count]; i++) {
        NSMutableArray *test = [[NSMutableArray alloc] init];
        [arrayData addObject:test];
    }
    // self.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"More" style:UIBarButtonItemStyleBordered target:self action:@selector(loadMore)];
    
    waterFlow_self = [[WaterFlowView alloc] initWithFrame:CGRectMake(0, 115, 320, 460-44-115)];
    waterFlow_self.waterFlowViewDelegate = self;
    waterFlow_self.waterFlowViewDatasource = self;
    waterFlow_self.tag = 0;
    waterFlow_self.backgroundColor = [UIColor whiteColor];
    
    waterFlow_others = [[WaterFlowView alloc] initWithFrame:CGRectMake(0, 115, 320, 460-44-115)];
    waterFlow_others.waterFlowViewDelegate = self;
    waterFlow_others.waterFlowViewDatasource = self;
    waterFlow_others.tag = 1;
    waterFlow_others.backgroundColor = [UIColor whiteColor];
    [self.view addSubview:waterFlow_others];
    [self.view addSubview:waterFlow_self];
    
    [self loadInternetData];
    [super viewDidAppear:animated];
}

- (void)viewDidUnload
{
    //[self setBs_id:nil];
    [self setName:nil];
    [self setAvatar:nil];
    [self setTags:nil];
    [self setIntroduction:nil];
    [self setSelfButton:nil];
    [self setOthersButton:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

@end
